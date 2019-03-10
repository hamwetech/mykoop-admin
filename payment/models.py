# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from coop.models import CooperativeMember, Cooperative

class PaymentAPI():
    pass


class BulkPaymentRequest(models.Model):
    file_name = models.CharField(max_length=255)
    cooperative = models.ForeignKey(Cooperative, blank=True, null=True, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=32, decimal_places=2)
    payment_method = models.CharField(max_length=18)
    status = models.CharField(max_length=10, choices=(('PROCESSING', 'PROCESSING'),
        ('COMPLETED', 'COMPLETED'), ('FAILED', 'FAILED'), ('CANCELED', 'CANCELED')))
    created_by = models.ForeignKey(User)
    create_Date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "bulk_payment_request"
    
    def get_log(self):
        return BulkPaymentRequestLog.objects.filter(bulk_payment_request=self)
    
    
class BulkPaymentRequestLog(models.Model):
    bulk_payment_request = models.ForeignKey(BulkPaymentRequest, on_delete=models.CASCADE)
    member = models.ForeignKey(CooperativeMember)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    payment_method = models.CharField(max_length=18)
    transaction_date = models.DateField()
    process_state = models.CharField(max_length=10, choices=(('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'),
        ('COMPLETED', 'COMPLETED'), ('FAILED', 'FAILED'), ('CANCELED', 'CANCELED')))
    created_by = models.ForeignKey(User)
    create_Date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bulk_payment_request_log'


class MemberPayment(models.Model):
    transaction_id = models.CharField(max_length=255)
    cooperative = models.ForeignKey(Cooperative)
    payemnt_reference = models.CharField(max_length=255, blank=True,)
    member = models.ForeignKey(CooperativeMember)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=10, choices=(('CASH', 'CASH'), ('BANK', 'BANK'), ('MOBILE MONEY', 'MOBILE MONEY')))
    user = models.ForeignKey(User, blank=True)
    status = models.CharField(max_length=15, choices=(('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')), blank=True)
    request = models.TextField(blank=True)
    response = models.TextField(blank=True)
    response_date = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "member_payment"
        
    def __unicode__(self):
        return self.member
    

class MobileMoneyRequest(models.Model):
    transaction_reference = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=25)
    member = models.ForeignKey(CooperativeMember, blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    status = models.CharField(max_length=15, choices=(('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')), blank=True)
    request = models.TextField(blank=True)
    response = models.TextField(blank=True)
    response_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "mobile_money_request"
        
    def __unicode__(self):
        return self.member
    
    
class MemberPaymentTransaction(models.Model):
    cooperative = models.ForeignKey(Cooperative, blank=True, null=True)
    member = models.ForeignKey(CooperativeMember, blank=True, null=True)
    payment_date = models.DateTimeField()
    transaction_reference = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=16, choices=(('CASH', 'CASH'), ('BANK', 'BANK'), ('MOBILE MONEY', 'MOBILE MONEY')))
    status = models.CharField(max_length=15, choices=(('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')), blank=True)
    balance_before = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    balance_after = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "member_payment_transaction"
        
    def __unicode__(self):
        return "%s" % self.transaction_reference
    
    
