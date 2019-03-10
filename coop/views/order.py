from __future__ import unicode_literals
import json
import datetime
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms.formsets import formset_factory, BaseFormSet
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from coop.models import MemberOrder, CooperativeMember
from coop.forms import OrderItemForm, MemberOrderForm
from coop.views.member import save_transaction
from conf.utils import generate_alpanumeric, genetate_uuid4, log_error, log_debug, generate_numeric, float_to_intstring, get_deleted_objects,\
get_message_template as message_template

class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        
        context.update(self.extra_context)
        return context
    
    
class MemberOrderListView(ExtraContext, ListView):
    model = MemberOrder
    ordering = ['-create_date']
    extra_context = {'active': ['_order']}
    
    def get_queryset(self):
        queryset = super(MemberOrderListView, self).get_queryset()
        
        if not self.request.user.profile.is_union():
            if not self.request.user.profile.is_partner():
                cooperative = self.request.user.cooperative_admin.cooperative 
                queryset = queryset.filter(member__cooperative=cooperative)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(MemberOrderListView, self).get_context_data(**kwargs)
        return context
    
    

class MemberOrderCreateView(View):
    template_name = 'coop/order_item_form.html'
    
    def get(self, request, *args, **kwargs):
        
        pk = self.kwargs.get('pk')
        prod = None
        var = None
        initial = None
        extra=1
       
        form = MemberOrderForm(request=request)
        order_form = formset_factory(OrderItemForm, formset=BaseFormSet, extra=extra)
        order_formset = order_form(prefix='order', initial=initial)
        data = {
            'order_formset': order_formset,
            'form': form,
            'active': ['_order'],
        }
        return render(request, self.template_name, data)
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        prod = None
        var = None
        initial = None
        extra=1
        form = MemberOrderForm(request.POST, request=request)
        order_form = formset_factory(OrderItemForm, formset=BaseFormSet, extra=extra)
        order_formset = order_form(request.POST, prefix='order', initial=initial)
        try:
            with transaction.atomic():
                if form.is_valid() and order_formset.is_valid():
                    mo = form.save(commit=False)
                    mo.order_reference = generate_numeric(8, '30')
                    mo.created_by = request.user
                    mo.save()
                    price = 0
                    for orderi in order_formset:
                        os = orderi.save(commit=False)
                        os.order = mo
                        os.unit_price = os.item.price
                        os.created_by = request.user
                        os.save()
                        price += os.price
                    mo.order_price = price
                    mo.save()
                    return redirect('coop:order_list')
        except Exception as e:
            log_error()
        data = {
            'order_formset': order_formset,
            'form': form,
            'active': ['_order'],
        }
        return render(request, self.template_name, data)
    
class MemberOrderDetailView(ExtraContext, DetailView):
    model = MemberOrder
    extra_context = {'active': ['_order']}
    
    
class MemberOrderDeleteView(ExtraContext, DeleteView):
    model = MemberOrder
    extra_context = {'active': ['_order']}
    success_url = reverse_lazy('coop:order_list')
    
    def get_context_data(self, **kwargs):
        #
        context = super(MemberOrderDeleteView, self).get_context_data(**kwargs)
        #
        
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        #
        return context
    

class MemberOrderStatusView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        status = self.kwargs.get('status')
        today = datetime.datetime.today()
        try:
            mo = MemberOrder.objects.get(pk=pk)
            if status == 'ACCEPT':
                mo.accept_date = today
            if status == 'SHIP':
                mo.ship_date = today
            if status == 'ACCEPT_DELIVERY':
                mo.delivery_accept_date = today
            if status == 'REJECT_DELIVERY':
                mo.delivery_reject_date = today
            if status == 'COLLECTED':
                mo.collect_date = today
            mo.status = status
            mo.save()
        except Exception as e:
            log_error()
        
        return redirect('coop:order_list')
    
