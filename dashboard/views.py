# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import TemplateView
from django.db.models import Q, CharField, Max, Value as V
from django.db.models.functions import Concat
from system.models import Union, CooperativeMember, MemberOrder
from collections import Counter
from django.db.models import Count


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
        farmers = list()
        orders_count = []
        for u in unions:
            queryset = CooperativeMember.objects.using(u.name.lower()).all()
            d = date.today() - timedelta(days=8900)
            date_ = d.strftime("%Y-%m-%d")
            male = queryset.filter(Q(gender__iexact='Male')|Q(gender__iexact='M'))
            female = queryset.filter(Q(gender__iexact='Female')|Q(gender__iexact='F'))
            refugee = queryset.filter(is_refugee=True)
            my = 0
            fy = 0
            for q in male:
                if q.age() >= 13 and q.age() <= 25:
                    my += 1
            myouth += my

            for q in female:
                if q.age() >= 13 and q.age() <= 25:
                    fy += 1
            fyouth += fy

            amale = male.filter(date_of_birth__lte=d)
            afemale = female.filter(date_of_birth__lte=d)

            mc += amale.count()
            fc += afemale.count()
            rc += refugee.count()

            mb.append({'union': u.name, 'count': queryset.count(),
                       'male': mc, 'female': fc,
                       'refugee': refugee.count(), 'myouth': my, 'fyouth': fy
                       })
            members.extend(queryset)

            aq = CooperativeMember.objects.using(u.name.lower()).values('district__name').annotate(Sum('land_acreage')).filter(district__name__in=districts)
            fq = CooperativeMember.objects.using(u.name.lower()).values('district__name').annotate(total=Count('id')).filter(district__name__in=districts).order_by('total')
            ord = MemberOrder.objects.using(u.name.lower()).all()
            orders_count.append({'union': u.name, 'count': ord.count()})
            acreage.extend(aq)
            farmers.extend(fq)

        cooperatives = []
        cp = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/cooperative/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            r = requests.post(url, headers=header, verify=False)

            if r:
                cp.append({'union': u.name, 'count': len(r.json())})
                cooperatives.extend(r.json())

        ag = []
        for u in unions:
            token = u.token
            url = '%s/endpoint/user/list/' % u.url
            header = {'Authorization': 'Token %s' % token}
            r = requests.post(url, headers=header, verify=False)
            if r:
                ag.append({'union': u.name, 'count': len(r.json())})
                agents.extend(r.json())

        import pandas as pd
        df = pd.DataFrame(acreage)
        f = pd.DataFrame(farmers)
        g = df.groupby('district__name', as_index=False).sum()
        ff = f.groupby('district__name', as_index=False).sum()
        d = g.to_dict('r')
        dd = ff.to_dict('r')

        context['union_count'] = unions.count()
        context['cooperative_count'] = len(cooperatives)
        context['agent_count'] = len(agents)
        context['coop_lst'] = cp
        context['agent_lst'] = ag
        context['member_lst'] = mb
        context['member_count'] = len(members)
        context['male'] = mc
        context['female'] = fc
        context['myouth'] = myouth
        context['fyouth'] = fyouth
        context['refugee'] = rc
        context['acreage'] = d
        context['farmers'] = dd
        context['orders_count'] = orders_count
        return context