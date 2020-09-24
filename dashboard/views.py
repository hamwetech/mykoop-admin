# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import TemplateView
from django.db.models import Q, CharField, Max, Value as V
from django.db.models.functions import Concat
from system.models import Union
from collections import Counter

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        unions = Union.objects.all()
        cooperative = 'all'
        members = []
        agents = []
        mb = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/member/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            payload = {'cooperative': cooperative}
            r = requests.post(url, headers=header, data=payload)

            if r:
                m = Counter()
                f = Counter()
                y = Counter()
                ref = Counter()

                for item in r.json():
                    for key, value in item.items():
                        if key == "gender":
                            if value:
                                if value.lower() == "female":
                                    f.update([value])
                                if value.lower() == "male":
                                    m.update([value])
                        if key == "age":
                            if value:
                                if value >= 15 and value <= 35:
                                    y.update([key])

                        if key == "is_refugee":
                            if value:
                                ref.update([key])

                mb.append({'union': u.name, 'count': len(r.json()), 'male': m['Male'], 'female': f['Female'], 'refugee': ref['is_refugee'], 'youth': y['age']})
                members.extend(r.json())

        cooperatives = []
        cp = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/cooperative/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            r = requests.post(url, headers=header)

            if r:
                cp.append({'union': u.name, 'count': len(r.json())})
                cooperatives.extend(r.json())

        ag = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/user/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            r = requests.post(url, headers=header)
            if r:
                ag.append({'union': u.name, 'count': len(r.json())})
                agents.extend(r.json())


        male = Counter()
        female = Counter()
        youth = Counter()
        refugee = Counter()

        for item in members:
            for key, value in item.items():
                if key == "gender":
                    if value:
                        if value.lower() == "female":
                            female.update([value])
                        if value.lower() == "male":
                            male.update([value])
                if key == "age":
                    if value:
                        if value >= 15 and value <= 35:
                            youth.update([key])

                if key == "is_refugee":
                    if value:
                        refugee.update([key])

        context['union_count'] = unions.count()
        context['cooperative_count'] = len(cooperatives)
        context['member_count'] = len(members)
        context['agent_count'] = len(agents)
        context['member_lst'] = mb
        context['coop_lst'] = cp
        context['agent_lst'] = ag
        context['male'] = male['Male']
        context['female'] = female['Female']
        context['youth'] = youth['age']
        context['refugee'] = refugee['is_refugee']
        return context
    
    


