# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import string
import random
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.forms.models import model_to_dict
from django.contrib.auth import authenticate

from conf.utils import generate_alpanumeric

from userprofile.models import Profile
from product.models import ProductVariation, ProductVariationPrice
from conf.models import District, County, SubCounty, Village
from coop.models import CooperativeMember
from activity.models import ThematicArea, TrainingModule, TrainingAttendance
from endpoint.serializers import *


class Login(APIView):

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = request.data
                cooperative = False
                username = data.get('username')
                password = data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    if hasattr(user.profile.access_level, 'name'):
                        if user.profile.access_level.name.lower()  == "cooperative" and user.cooperative_admin:
                            cooperative = True
                        if cooperative:
                            q_token = Token.objects.filter(user=user)
                            if q_token.exists():
                                
                                token = q_token[0]
                                qs = Profile.objects.get(user=user)
                                product = Product.objects.values('name').all()
                                breed = ProductVariation.objects.values('id', 'name').all()
                                district = District.objects.values('id', 'name').all()
                                county = County.objects.values('id', 'district', 'name').all()
                                sub_county = SubCounty.objects.values('id', 'county', 'name').all()
                                thematic_area = ThematicArea.objects.values('id', 'thematic_area').all()
                                
                                return Response({
                                    "status": "OK",
                                    "token": token.key,
                                    "cooperative": {"name": user.cooperative_admin.cooperative.name,
                                                    "id": user.cooperative_admin.cooperative.id},
                                    "product": product,
                                    "breeds": breed,
                                    "district": district,
                                    "county": county,
                                    "sub_county": sub_county,
                                    "thematic_area": thematic_area,
                                    "response": "Login success"
                                    }, status.HTTP_200_OK)
                            return Response({"status": "ERROR", "response": "Access Denied"}, status.HTTP_200_OK)
                        
                return Response({"status": "ERROR", "response": "Invalid Username or Password"}, status.HTTP_200_OK)
        except Exception as err:
            return Response({"status": "ERROR", "response": err}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberEndpoint(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        member = MemberSerializer(data=request.data)
        business = CooperativeMemberBusinessSerializer(data=request.data)
        supply = CooperativeMemberSupplySerializer(data=request.data)
        product = CooperativeMemberProductDefinitionSerializer(data=request.data)
        quantity = CooperativeMemberProductQuantitySerializer(data=request.data)
        
        try:
            if member.is_valid():
                if business.is_valid():
                    if supply.is_valid():
                        if product.is_valid():
                            if quantity.is_valid():
                                with transaction.atomic():
                                    __member = member.save()
                                    __member.member_id = self.generate_member_id(__member.cooperative)
                                    __member.save()
                                    __business = business.save()
                                    __business.cooperative_member = __member
                                    __business.save()
                                    __supply = supply.save()
                                    __supply.cooperative_member = __member
                                    __supply.save()
                                    __product = product.save()
                                    __product.cooperative_member = __member
                                    __product.save()
                                    
                                    breeds = request.data.get('breeds')
                                    if breeds:
                                        breed = [ x if x else None  for b in breeds for x in ProductVariation.objects.filter(name=b.strip()) ]
                                        __product.product_variation.add(*breed)
                                    
                                    return Response(
                                        {"status": "OK", "response": "Farmer Profile Saved Successfully"},
                                        status.HTTP_200_OK)
            #return Response(member.errors+business.errors+supply.errors+product.errors+quantity.errors)
                            return Response(quantity.errors)
                        return Response(product.errors)
                    return Response(supply.errors)
                return Response(business.errors)
            return Response(member.errors)
        except Exception as err:
            return Response({"status": "ERROR", "response": err}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(supply.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def safe_get(self, _model, _value):
        try:
            return get_object_or_404(_model, cooperative_member=_value)
        except Exception:
            return None
    
    def generate_member_id(self, cooperative):
        member = CooperativeMember.objects.all()
        count = member.count() + 1
        
        today = datetime.today()
        datem = today.year
        yr = str(datem)[2:]
        # idno = generate_numeric(size=4, prefix=str(m.cooperative.code)+yr)
        # fint = "%04d"%count
        # idno = str(cooperative.code)+yr+fint
        # member = member.filter(member_id=idno)
        idno = self.check_id(member, cooperative, count, yr)
        log_debug("Cooperative %s code is %s" % (cooperative.code, idno))
        return idno
    
    def check_id(self, member, cooperative, count, yr):
        fint = "%04d"%count
        idno = str(cooperative.code)+yr+fint
        member = member.filter(member_id=idno)
        if member.exists():
            count = count + 1
            print "iteration count %s" % count
            return self.check_id(member, cooperative, count, yr)
        return idno
    
    
class MemberList(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, member=None, format=None):
        members = CooperativeMember.objects.filter(cooperative=request.user.cooperative_admin.cooperative).order_by('-surname')
        if member:
            members = members.filter(Q(member_id=member)|Q(phone_number=member)|Q(other_phone_number=member))
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    

class TrainingSessionView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        module = TrainingModuleSerializer(data=request.data)
        training = TrainingSessionSerializer(data=request.data)
        try:
            if module.is_valid():
                if training.is_valid():
                    with transaction.atomic():
                        __module = module.save()
                        __module.created_by = request.user
                        __module.save()
                        __training = training.save()
                        __training.training_module = __module
                        __training.trainer = request.user
                        __training.created_by = request.user
                        __training.training_reference = generate_alpanumeric(prefix="TR", size=8)
                        __training.save()
                        
                        #get Member list
                        data = request.data
                        for m in data.get('member'):
                            member = CooperativeMember.objects.get(member_id=m)
                            __training.coop_member.add(member)
                        
                        return Response(
                            {"status": "OK", "response": "Training Session Saved"},
                            status.HTTP_200_OK)
            
                return Response(training.errors)
            return Response(module.errors)
        except Exception as err:
            return Response({"status": "ERROR", "response": err}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(supply.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TrainingSessionListView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        training = TrainingSession.objects.all().order_by('-create_date')
        serializer = TrainingSessionSerializer(training, many=True)
        return Response(serializer.data)

