# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from coop.models import CooperativeMember, Cooperative
from product.models import ProductVariation

class ThematicArea(models.Model):
    thematic_area = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'thematic_area'
        
    def __unicode__(self):
        return self.thematic_area


class TrainingModule(models.Model):
    thematic_area = models.ForeignKey(ThematicArea)
    topic = models.CharField(max_length=250)
    descriprion = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_module'
        
    def __unicode__(self):
        return self.module


class TrainingAttendance(models.Model):
    training_module = models.ForeignKey(TrainingModule, null=True, blank=True)
    training_reference = models.CharField(max_length=256, null=True, blank=True)
    trainer = models.ForeignKey(User, related_name='trainer')
    coop_member = models.ManyToManyField(CooperativeMember, blank=True)
    gps_location = models.CharField(max_length=256, null=True, blank=True)
    training_start = models.DateTimeField()
    training_end = models.DateTimeField()
    created_by = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_attendance'
        
    def __unicode__(self):
        return self.coop_member
    
    def trainer_is_cooperative(self):
        if self.trainer.cooperative_admin:
            return True
        return False
    
    
class TrainingSession(models.Model):
    thematic_area = models.ForeignKey(ThematicArea, null=True, blank=True)
    training_reference = models.CharField(max_length=256, null=True, blank=True)
    trainer = models.ForeignKey(User, related_name='training_officer', null=True, blank=True)
    topic = models.CharField(max_length=256, null=True, blank=True)
    descriprion = models.TextField(null=True, blank=True)
    cooperative = models.ForeignKey(Cooperative, null=True, blank=True)
    coop_member = models.ManyToManyField(CooperativeMember, blank=True)
    gps_location = models.CharField(max_length=256, null=True, blank=True)
    training_start = models.DateTimeField()
    training_end = models.DateTimeField()
    created_by = models.ForeignKey(User, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_session'
        
    def __unicode__(self):
        return self.coop_member
    
 
class Visit(models.Model):
    coop_member = models.ForeignKey(CooperativeMember)
    visit_date = models.DateField()
    reason = models.CharField(max_length=160)
    description = models.TextField(null=True, blank=True)
    gps_coodinates = models.CharField(max_length=256, null=True, blank=True)
    created_by = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'partner_visit'
        
    def __unicode__(self):
        return self.coop_member
