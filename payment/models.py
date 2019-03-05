# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from coop.models import CooperativeMember, Cooperative

class PaymentAPI():
    pass


class MemberPayment(models.Model):
    transaction_id = models.CharField(max_length=255)
    cooperative = models.ForeignKey(Cooperative)
    member = models.ForeignKey(CooperativeMember)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=10, choices=(('CASH', 'CASH'), ('BANK', 'BANK'), ('MOBILE MONEY', 'MOBILE MONEY')))
    user = models.ForeignKey(User, blank=True)
    status = models.CharField(max_length=15, choices=(('PENDING', 'PENDING'), ('SUCCESSFULL', 'SUCCESSFULL'), ('FAILED', 'FAILED')), blank=True)
    request = models.TextField(blank=True)
    response = models.TextField(blank=True)
    response_date = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "member_payment"
        
    def __unicode__(self):
        return self.member
    
