# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q, CharField, Max, Value as V

from system.models import Union, CooperativeMember
from system.form import UnionForm, MemberProfileSearchForm


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
            r = requests.post(url, headers=header)

            if r:
                cooperatives.extend(r.json())
        context['object_list'] = cooperatives
        return context


class MembersListView(TemplateView):

    template_name = "members_list.html"

    def get_context_data(self, **kwargs):
        context = super(MembersListView, self).get_context_data(**kwargs)
        msisdn = self.request.GET.get('phone_number')
        name = self.request.GET.get('name')
        coop = self.request.GET.get('cooperative')
        role = self.request.GET.get('role')
        district = self.request.GET.get('district')
        u = self.request.GET.get('union')
        unions = Union.objects.all()
        if u:
            unions = Union.objects.filter(pk=u)
        members = list()
        cooperative = 'all'
        for u in unions:
            #     token = u.token
            #     url = '%s/endpoint/member/list/' % u.url
            #     header = {'Authorization': 'Token %s' % token}
            #     payload = {'cooperative': cooperative}
            #     r = requests.post(url, headers=header, data=payload)
            #
            queryset = CooperativeMember.objects.using(u.name.lower()).all()
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
            if queryset:
                members.extend(queryset)


        context['object_list'] = members
        context['form'] = MemberProfileSearchForm(self.request.GET, request=self.request)
        return context


class AgentListView(TemplateView):

    template_name = "agents_list.html"

    def get_context_data(self, **kwargs):
        context = super(AgentListView, self).get_context_data(**kwargs)
        unions = Union.objects.all()
        members = []
        cooperative = 'all'
        for u in unions:
            token = u.token
            url = '%s/endpoint/user/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            r = requests.post(url, headers=header)
            if r:
                members.extend(r.json())
        context['object_list'] = members
        return context
