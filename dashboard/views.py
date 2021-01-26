# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import TemplateView
from django.db.models import Q, CharField, Max, Value as V
from django.db.models.functions import Concat
from system.models import Union, CooperativeMember
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
        districts = ['Guli',  'Kitgum', 'Lamwo', 'Pader', 'Agago', 'Amuru', 'Nwoya', 'Omoro', 'Amuru', 'Alebtong', 'Amolatar', 'Apac', 'Dokolo', 'Kole', 'Lira', 'Oyam', 'Otuke', 'Kwania', 'Kiryaongo']
        youth = 0
        myouth = 0
        fyouth = 0
        mc = 0
        fc = 0
        rc = 0
        acreage = list()
        for u in unions:
            queryset = CooperativeMember.objects.using(u.name.lower()).all()
            male = queryset.filter(gender__iexact='Male')
            female = queryset.filter(gender__iexact='Female')
            refugee = queryset.filter(is_refugee=True)
            y = 0
            my = 0
            fy = 0
            for q in queryset:
                if q.age() >= 15 and q.age() <= 35:
                    y += 1

            for qm in male:
                if qm.age() >= 15 and qm.age() <= 35:
                    my += 1

            for qf in female:
                if qf.age() >= 15 and qf.age() <= 35:
                    fy += 1

            youth += y
            myouth += my
            fyouth += fy

            mc += male.count()
            fc += female.count()
            rc += refugee.count()

            mb.append({'union': u.name, 'count': queryset.count(),
                       'male': male.count(), 'female': female.count(),
                       'refugee': refugee.count(), 'youth': y
                       })
            members.extend(queryset)

            aq = CooperativeMember.objects.using(u.name.lower()).values('district__name').annotate(Sum('land_acreage')).filter(district__name__in=districts)
            acreage.extend(aq)

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

        context['union_count'] = unions.count()
        context['cooperative_count'] = len(cooperatives)
        context['agent_count'] = len(agents)
        context['coop_lst'] = cp
        context['agent_lst'] = ag
        context['member_lst'] = mb
        context['member_count'] = len(members)
        context['male'] = mc
        context['female'] = fc
        context['youth'] = youth
        context['myouth'] = myouth
        context['fyouth'] = fyouth
        context['refugee'] = rc
        context['acreage'] = acreage
        return context
    
    


