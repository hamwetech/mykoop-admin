# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from coop.models import Collection, CooperativeMember
from coop.forms import CollectionForm
from coop.views.member import save_transaction
from conf.utils import generate_alpanumeric, genetate_uuid4

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_collection']
        context.update(self.extra_context)
        return context

class CollectionListView(ExtraContext, ListView):
    model = Collection
    extra_context = {'active': ['_collection']}
    
class CollectionCreateView(ExtraContext, CreateView):
    model = Collection
    extra_context = {'active': ['_collection']}
    form_class = CollectionForm
    success_url = reverse_lazy('coop:collection_list')
    
    def form_valid(self, form):
        form.instance.collection_reference = genetate_uuid4()
        form.instance.created_by = self.request.user
        
        params = {'amount': form.instance.total_price,
                  'member': form.instance.member,
                  'transaction_reference': form.instance.collection_reference ,
                  'transaction_type': 'COLLECTION',
                  'entry_type': 'CREDIT'
                  }
        member = CooperativeMember.objects.filter(pk=form.instance.member.id)
        if member.exists():
            member = member[0]
            qty_bal = member.collection_quantity if member.collection_quantity else 0
            
            new_bal = form.instance.quantity + qty_bal
            member.collection_quantity = new_bal
            member.save()
        save_transaction(params)
        member = super(CollectionCreateView, self).form_valid(form)
        return member
    
    
        
    
class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    extra_context = {'active': ['_collection', '__createcc']}
    success_url = reverse_lazy('activity:collection_create')
    
    def form_valid(self, form):
        form.instance.collection_reference = genetate_uuid4()
        return super(CollectionUpdateView, self).form_valid(form)