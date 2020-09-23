# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import TemplateView
from django.db.models import Q, CharField, Max, Value as V
from django.db.models.functions import Concat
from system.models import Union

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        unions = Union.objects.all()
        cooperative = 'all'
        members = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/member/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            payload = {'cooperative': cooperative}
            r = requests.post(url, headers=header, data=payload)

            if r:
                members.extend(r.json())

        cooperatives = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/cooperative/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            r = requests.post(url, headers=header)

            if r:
                cooperatives.extend(r.json())

        context['union_count'] = unions.count()
        context['cooperative_count'] = len(cooperatives)
        context['member_count'] = len(members)
        return context
    
    


