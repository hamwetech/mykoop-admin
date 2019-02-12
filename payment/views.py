# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import xlwt
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, HttpResponse

from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from payment.forms import MemberPaymentForm
from payment.models import MemberPayment
from payment.utils import payment_tranasction
from conf.utils import generate_alpanumeric

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_collection']
        context.update(self.extra_context)
        return context
    

class PaymentMethodListView(ExtraContext, ListView):
    model = MemberPayment
    extra_context = {'active': ['_payment']}
    
    
class PaymentMethodCreateView(ExtraContext, CreateView):
    model = MemberPayment
    form_class = MemberPaymentForm
    extra_context = {'active': ['_payment']}
    success_url = reverse_lazy('payment:list')
    
    def form_valid(self, form):
        reference = generate_alpanumeric()
        form.instance.user = self.request.user
        form.instance.transaction_id = reference
        msisdn = form.instance.member.phone_number
        amount = form.instance.amount
        res = payment_tranasction(msisdn, amount, reference)
        form.instance.status = res['status']
        form.instance.response = res
        form.instance.response_date = datetime.datetime.now()
        return super(PaymentMethodCreateView, self).form_valid(form)
    

class PaymentMethodUpateView(UpdateView):
    model = MemberPayment
    
    
class DownloadPaymentExcelView(View):
    
    def get(self, request, *args, **kwargs):
        _choices = ['id','cooperative__name', 'member__member_id', 'amount', 'transaction_id', 'status']
        columns = []
        columns += [self.replaceMultiple(c, ['_', '__name'], ' ').title() for c in _choices]
        
        #Gather the Information Found
        # Create the HttpResponse object with Excel header.This tells browsers that 
        # the document is a Excel file.
        response = HttpResponse(content_type='application/ms-excel')
        
        # The response also has additional Content-Disposition header, which contains 
        # the name of the Excel file.
        response['Content-Disposition'] = 'attachment; filename=MembersPayment_%s.xls' % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
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
        
       
        _payment = MemberPayment.objects.values(*_choices).all()
        
        for m in _payment:
            row_num += 1
            row = [m['%s' % x] for x in _choices]
            for col_num in range(len(row)):
                worksheet.write(row_num, col_num, row[col_num])
        workbook.save(response)
        return response
    
    def replaceMultiple(self, mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces :
            # Check if string is in the main string
            if elem in mainString :
                # Replace the string
                mainString = mainString.replace(elem, newString)
        
        return  mainString