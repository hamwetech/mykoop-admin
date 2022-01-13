# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import xlrd
import xlwt
import csv
from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q, CharField, Max, Value as V

from system.models import Union, CooperativeMember, MemberOrder
from system.form import UnionForm, MemberProfileSearchForm, AgentSearchForm, MemberOrderSearchForm
from conf.utils import log_debug, log_error, generate_alpanumeric, float_to_intstring, get_deleted_objects,\
get_message_template as message_template


class ExtraContext(object):
    extra_context = {}
    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class UnionListView(ListView):
    template_name = "unoin_list.html"
    model = Union


class UnionCreateView(ExtraContext, CreateView):
    model = Union
    form_class = UnionForm
    extra_context = {'active': ['_union']}
    success_url = reverse_lazy('union_list')


class UnionUpdateView(ExtraContext, UpdateView):
    model = Union
    form_class = UnionForm
    extra_context = {'active': ['_union']}
    success_url = reverse_lazy('union_list')


class UnionDeleteView(ExtraContext, DeleteView):
    model = Union
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('union_list')

    def get_context_data(self, **kwargs):
        #
        context = super(UnionDeleteView, self).get_context_data(**kwargs)
        #

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        #
        return context


class CooperativesListView(TemplateView):

    template_name = "cooperative_list.html"

    def get_context_data(self, **kwargs):
        context = super(CooperativesListView, self).get_context_data(**kwargs)
        unions = Union.objects.all()
        cooperatives = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/cooperative/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            r = requests.post(url, headers=header, verify=False)

            if r:
                cooperatives.extend(r.json())
        context['object_list'] = cooperatives
        return context


class MembersListView(TemplateView):

    template_name = "members_list.html"

    def dispatch(self, *args, **kwargs):

        if self.request.GET.get('download'):
            return self.download_file()
        if self.request.GET.get('csv'):
            return self.download_csv()
        return super(MembersListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MembersListView, self).get_context_data(**kwargs)
        msisdn = self.request.GET.get('phone_number')
        name = self.request.GET.get('name')
        coop = self.request.GET.get('cooperative')
        role = self.request.GET.get('role')
        district = self.request.GET.get('district')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        un = self.request.GET.get('union')
        unions = Union.objects.all()
        if un:
            unions = Union.objects.filter(pk=un)
        members = list()
        cooperative = 'all'
        for u in unions:
            #     token = u.token
            #     url = '%s/endpoint/member/list/' % u.url
            #     header = {'Authorization': 'Token %s' % token}
            #     payload = {'cooperative': cooperative}
            #     r = requests.post(url, headers=header, data=payload)
            #
            queryset = CooperativeMember.objects.using(u.name.lower()).all().order_by('-create_date')
            if msisdn:
                queryset = queryset.filter(msisdn=msisdn)
            if name:
                # name=Concat('surname',V(' '),'first_name',V(' '),'other_name')
                queryset = queryset.filter(
                    Q(surname__icontains=name) | Q(first_name__icontains=name) | Q(other_name=name))
                # queryset = queryset.filter(Concat(surname,V(' '),first_name,V(' '),other_name)=name)
            if coop:
                queryset = queryset.filter(cooperative__id=coop)
            if role:
                queryset = queryset.filter(coop_role=role)
            if district:
                queryset = queryset.filter(district__id=district)
            if start_date:
                queryset = queryset.filter(create_date__gte = start_date)
            if end_date:
                queryset = queryset.filter(create_date__lte = end_date)
            if queryset:
                members.extend(queryset)
        context['object_list'] = members
        context['form'] = MemberProfileSearchForm(self.request.GET, request=self.request)
        return context

    def download_file(self, *args, **kwargs):

        _value = []
        columns = []
        msisdn = self.request.GET.get('phone_number')
        name = self.request.GET.get('name')
        coop = self.request.GET.get('cooperative')
        role = self.request.GET.get('role')
        district = self.request.GET.get('district')

        profile_choices = ['id', 'cooperative__name', 'member_id', 'surname', 'first_name', 'other_name',
                           'date_of_birth', 'gender', 'is_refugee', 'maritual_status', 'phone_number', 'email',
                           'district__name', 'sub_county__name', 'village', 'address', 'gps_coodinates',
                           'coop_role', 'shares',
                           'collection_amount', 'collection_quantity', 'paid_amount', 'create_by__first_name', 'create_by__last_name', 'create_date']

        columns += [self.replaceMultiple(c, ['_', '__name'], ' ').title() for c in profile_choices]
        # Gather the Information Found
        # Create the HttpResponse object with Excel header.This tells browsers that
        # the document is a Excel file.
        response = HttpResponse(content_type='application/ms-excel')

        # The response also has additional Content-Disposition header, which contains
        # the name of the Excel file.
        response['Content-Disposition'] = 'attachment; filename=CooperativeMembers_%s.xls' % datetime.now().strftime(
            '%Y%m%d%H%M%S')

        # Create object for the Workbook which is under xlwt library.
        workbook = xlwt.Workbook()

        # By using Workbook object, add the sheet with the name of your choice.
        worksheet = workbook.add_sheet("Members")

        row_num = 0
        style_string = "font: bold on; borders: bottom dashed"
        style = xlwt.easyxf(style_string)

        for col_num in range(len(columns)):
            # For each cell in your Excel Sheet, call write function by passing row number,
            # column number and cell data.
            worksheet.write(row_num, col_num, columns[col_num], style=style)

        un = self.request.GET.get('union')
        unions = Union.objects.all()
        if un:
            unions = Union.objects.filter(pk=un)
        _members = list()
        cooperative = 'all'
        for u in unions:

            queryset = CooperativeMember.objects.values(*profile_choices).using(u.name.lower()).all()

            if msisdn:
                queryset = queryset.filter(phone_number='%s' % msisdn)
            if name:
                queryset = queryset.filter(Q(surname__icontains=name) | Q(first_name__icontains=name) | Q(other_name=name))
            if coop:
                queryset = queryset.filter(cooperative__id=coop)
            if role:
                queryset = queryset.filter(coop_role=role)
            if district:
                queryset = queryset.filter(district__id=district)
            if queryset:
                _members.extend(queryset)

        for m in _members:

            row_num += 1
            row_ = []
            for x in profile_choices:

                if m.get('%s' % x):
                    if 'date_of_birth' in x:
                        # row_.append(datetime.strpdate(str(m.get('%s' % x)), '%Y-%m-%d'))
                        row_.append(str(m.get('%s' % x)))
                    elif 'create_date' in x:
                        # row_.append(datetime.strptime(str(m.get('%s' % x))[:19], '%Y-%m-%d %H:%M:%S'))
                        row_.append(str(m.get('%s' % x))[:19])
                    elif 'union' in x:
                        row_.append(u.name)
                    else:
                        row_.append(m.get('%s' % x))
                else:
                    row_.append("")

            for col_num in range(len(row_)):
                worksheet.write(row_num, col_num, row_[col_num])
        workbook.save(response)
        return response

    def download_csv(self, *args, **kwargs):

        _value = []
        columns = []
        msisdn = self.request.GET.get('phone_number')
        name = self.request.GET.get('name')
        coop = self.request.GET.get('cooperative')
        role = self.request.GET.get('role')
        district = self.request.GET.get('district')

        profile_choices = ['id', 'cooperative__name', 'member_id', 'surname', 'first_name', 'other_name',
                           'date_of_birth', 'gender', 'is_refugee', 'maritual_status', 'phone_number', 'email',
                           'district__name', 'sub_county__name', 'village', 'address', 'gps_coodinates',
                           'coop_role', 'shares',
                           'collection_amount', 'collection_quantity', 'paid_amount', 'create_by__first_name', 'create_by__last_name', 'create_date']

        columns += [self.replaceMultiple(c, ['_', '__name'], ' ').title() for c in profile_choices]
        # Gather the Information Found
        # Create the HttpResponse object with Excel header.This tells browsers that
        # the document is a Excel file.
        response = HttpResponse(content_type='text/csv')

        # The response also has additional Content-Disposition header, which contains
        # the name of the Excel file.
        response['Content-Disposition'] = 'attachment; filename=CooperativeMembers_%s.csv' % datetime.now().strftime(
            '%Y%m%d%H%M%S')

        # Create object for the Workbook which is under xlwt library.
        # workbook = xlwt.Workbook()
        writer = csv.writer(response)

        # By using Workbook object, add the sheet with the name of your choice.
        # worksheet = workbook.add_sheet("Members")

        row_num = 0
        # style_string = "font: bold on; borders: bottom dashed"
        # style = xlwt.easyxf(style_string)

        # for col_num in range(len(columns)):
        #     # For each cell in your Excel Sheet, call write function by passing row number,
        #     # column number and cell data.
        #     writer.writerow(row_num, col_num, columns[col_num], style=style)

        writer.writerow(columns)

        un = self.request.GET.get('union')
        unions = Union.objects.all()
        if un:
            unions = Union.objects.filter(pk=un)
        _members = list()
        cooperative = 'all'
        for u in unions:

            queryset = CooperativeMember.objects.values(*profile_choices).using(u.name.lower()).all()

            if msisdn:
                queryset = queryset.filter(phone_number='%s' % msisdn)
            if name:
                queryset = queryset.filter(Q(surname__icontains=name) | Q(first_name__icontains=name) | Q(other_name=name))
            if coop:
                queryset = queryset.filter(cooperative__id=coop)
            if role:
                queryset = queryset.filter(coop_role=role)
            if district:
                queryset = queryset.filter(district__id=district)
            if queryset:
                _members.extend(queryset)

        for m in _members:

            row_num += 1
            row_ = []
            for x in profile_choices:

                if m.get('%s' % x):
                    if 'date_of_birth' in x:
                        # row_.append(datetime.strpdate(str(m.get('%s' % x)), '%Y-%m-%d'))
                        row_.append(str(m.get('%s' % x)))
                    elif 'create_date' in x:
                        # row_.append(datetime.strptime(str(m.get('%s' % x))[:19], '%Y-%m-%d %H:%M:%S'))
                        row_.append(str(m.get('%s' % x))[:19])
                    elif 'union' in x:
                        row_.append(u.name)
                    else:
                        row_.append(m.get('%s' % x.decode('ascii', 'ignore')))
                else:
                    row_.append("")

            writer.writerow(row_)
        return response

    def replaceMultiple(self, mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces:
            # Check if string is in the main string
            if elem in mainString:
                # Replace the string
                mainString = mainString.replace(elem, newString)

        return mainString

class AgentListView(TemplateView):

    template_name = "agents_list.html"

    def get_context_data(self, **kwargs):
        context = super(AgentListView, self).get_context_data(**kwargs)
        unions = Union.objects.all()
        members = []
        
        us = self.request.GET.get('union')
        end_date = self.request.GET.get('end_date')
        start_date = self.request.GET.get('start_date')
        payload = {"start_date": start_date, "end_date": end_date}
        if us:
            unions = unions.filter(pk=us)
        cooperative = 'all'
        for u in unions:
            token = u.token
            url = '%s/endpoint/user/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            
            r = requests.post(url, headers=header, data=payload, verify=False)
            if r:
                members.extend(r.json())
        context['object_list'] = members
        context['form'] = AgentSearchForm(self.request.GET, request=self.request)
        return context


class MembersOrderListView(TemplateView):

    template_name = "member_order_list.html"

    def dispatch(self, *args, **kwargs):

        if self.request.GET.get('download'):
            return self.download_file()
        return super(MembersOrderListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MembersOrderListView, self).get_context_data(**kwargs)
        msisdn = self.request.GET.get('phone_number')
        name = self.request.GET.get('name')
        coop = self.request.GET.get('cooperative')
        role = self.request.GET.get('role')
        district = self.request.GET.get('district')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        un = self.request.GET.get('union')
        agent = self.request.GET.get('agent')
        unions = Union.objects.all()
        if un:
            unions = Union.objects.filter(pk=un)
        orders = list()
        cooperative = 'all'
        for u in unions:
            #     token = u.token
            #     url = '%s/endpoint/member/list/' % u.url
            #     header = {'Authorization': 'Token %s' % token}
            #     payload = {'cooperative': cooperative}
            #     r = requests.post(url, headers=header, data=payload)
            #
            queryset = MemberOrder.objects.using(u.name.lower()).all().order_by('-create_date')
            if msisdn:
                queryset = queryset.filter(msisdn=msisdn)
            if name:
                # name=Concat('surname',V(' '),'first_name',V(' '),'other_name')
                queryset = queryset.filter(
                    Q(surname__icontains=name) | Q(first_name__icontains=name) | Q(other_name=name))
                # queryset = queryset.filter(Concat(surname,V(' '),first_name,V(' '),other_name)=name)
            if coop:
                queryset = queryset.filter(cooperative__id=coop)
            if role:
                queryset = queryset.filter(coop_role=role)
            if district:
                queryset = queryset.filter(district__id=district)
            if start_date:
                queryset = queryset.filter(create_date__gte = start_date)
            if end_date:
                queryset = queryset.filter(create_date__lte = end_date)
            if agent:
                queryset = queryset.filter(created_by__id=agent)
            if queryset:
                orders.extend(queryset)
        context['object_list'] = orders
        context['form'] = MemberOrderSearchForm(self.request.GET, request=self.request)
        return context

    def download_file(self, *args, **kwargs):

        _value = []
        columns = []
        msisdn = self.request.GET.get('phone_number')
        name = self.request.GET.get('name')
        coop = self.request.GET.get('cooperative')
        role = self.request.GET.get('role')
        district = self.request.GET.get('district')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        un = self.request.GET.get('union')
        agent = self.request.GET.get('agent')

        profile_choices = ['order_date', 'order_reference', 'member__member_id', 'member__first_name', 'member__surname', 'cooperative__name', 'order_price']

        columns += [self.replaceMultiple(c, ['_', '__name'], ' ').title() for c in profile_choices]
        # Gather the Information Found
        # Create the HttpResponse object with Excel header.This tells browsers that
        # the document is a Excel file.
        response = HttpResponse(content_type='application/ms-excel')

        # The response also has additional Content-Disposition header, which contains
        # the name of the Excel file.
        response['Content-Disposition'] = 'attachment; filename=CooperativeMembersOrders_%s.xls' % datetime.now().strftime(
            '%Y%m%d%H%M%S')

        # Create object for the Workbook which is under xlwt library.
        workbook = xlwt.Workbook()

        # By using Workbook object, add the sheet with the name of your choice.
        worksheet = workbook.add_sheet("Members")

        row_num = 0
        style_string = "font: bold on; borders: bottom dashed"
        style = xlwt.easyxf(style_string)

        for col_num in range(len(columns)):
            # For each cell in your Excel Sheet, call write function by passing row number,
            # column number and cell data.
            worksheet.write(row_num, col_num, columns[col_num], style=style)

        un = self.request.GET.get('union')
        unions = Union.objects.all()
        if un:
            unions = Union.objects.filter(pk=un)
        _members = list()
        cooperative = 'all'
        for u in unions:

            queryset = MemberOrder.objects.values(*profile_choices).using(u.name.lower()).all()

            if msisdn:
                queryset = queryset.filter(msisdn=msisdn)
            if name:
                # name=Concat('surname',V(' '),'first_name',V(' '),'other_name')
                queryset = queryset.filter(
                    Q(surname__icontains=name) | Q(first_name__icontains=name) | Q(other_name=name))
                # queryset = queryset.filter(Concat(surname,V(' '),first_name,V(' '),other_name)=name)
            if coop:
                queryset = queryset.filter(cooperative__id=coop)
            if role:
                queryset = queryset.filter(coop_role=role)
            if district:
                queryset = queryset.filter(district__id=district)
            if start_date:
                queryset = queryset.filter(create_date__gte=start_date)
            if end_date:
                queryset = queryset.filter(create_date__lte=end_date)
            if agent:
                queryset = queryset.filter(created_by__id=agent)

            if queryset:
                _members.extend(queryset)

        for m in _members:

            row_num += 1
            row_ = []
            for x in profile_choices:

                if m.get('%s' % x):
                    if 'date_of_birth' in x:
                        # row_.append(datetime.strpdate(str(m.get('%s' % x)), '%Y-%m-%d'))
                        row_.append(str(m.get('%s' % x)))
                    elif 'order_date' in x:
                        # row_.append(datetime.strptime(str(m.get('%s' % x))[:19], '%Y-%m-%d %H:%M:%S'))
                        row_.append(str(m.get('%s' % x))[:19])
                    elif 'union' in x:
                        row_.append(u.name)
                    else:
                        row_.append(m.get('%s' % x))
                else:
                    row_.append("")

            for col_num in range(len(row_)):
                worksheet.write(row_num, col_num, row_[col_num])
        workbook.save(response)
        return response

    def replaceMultiple(self, mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces:
            # Check if string is in the main string
            if elem in mainString:
                # Replace the string
                mainString = mainString.replace(elem, newString)

        return mainString
