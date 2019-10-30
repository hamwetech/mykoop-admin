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
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.forms.models import model_to_dict
from django.contrib.auth import authenticate

from userprofile.models import Profile
from product.models import ProductVariation, ProductVariationPrice
from conf.models import District, County, SubCounty, Village
from coop.models import Cooperative, CooperativeMember, Collection
from activity.models import ThematicArea, TrainingModule, TrainingAttendance
from endpoint.serializers import *

from coop.views.member import save_transaction
from conf.utils import generate_alpanumeric, genetate_uuid4, log_error, get_message_template as message_template
from coop.utils import sendMemberSMS



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
                #if hasattr(user.profile.access_level, 'name'):
                #if user.profile.access_level.name.lower()  == "cooperative" and user.cooperative_admin:
                #    cooperative = True
                #if cooperative:
                    q_token = Token.objects.filter(user=user)
                    if q_token.exists():
                        
                        token = q_token[0]
                        qs = Profile.objects.get(user=user)
                        product = Product.objects.values('name').all()
                        cooperatives = [{"id": c.id, "name": c.name} for c in Cooperative.objects.all()]
                        variation = ProductVariation.objects.values('id', 'product', 'name').all()
                        variation_price = ProductVariationPrice.objects.values('id', 'product', 'product__name', 'price').all()
                        district = District.objects.values('id', 'name').all()
                        county = County.objects.values('id', 'district', 'name').all()
                        sub_county = SubCounty.objects.values('id', 'county', 'name').all()
                        thematic_area = ThematicArea.objects.values('id', 'thematic_area').all()
                        user_type = user.profile.access_level.name.upper() if user.profile.access_level else "NONE"
                        is_admin = user.is_superuser
                        cooperative = None
                        if hasattr(user.profile.access_level, 'name'):
                            if user.cooperative_admin:
                                cooperative = {"name": user.cooperative_admin.cooperative.name,
                                                "id": user.cooperative_admin.cooperative.id}
                        return Response({
                            "status": "OK",
                            "token": token.key,
                            
                            "user": {"username": qs.user.username, "id": qs.user.id, "user_type": user_type, "is_admin": is_admin},
                            "cooperative": cooperative,
                            "cooperatives": cooperatives,
                            "product": product,
                            "variation": variation,
                            "variation_price": variation_price,
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
    parser_classes = [FormParser, MultiPartParser, FileUploadParser]
    
    def post(self, request, format=None):
        member = MemberSerializer(data=request.data)
        try:
            if member.is_valid():
                
                with transaction.atomic():
                    __member = member.save()
                    __member.member_id = self.generate_member_id(__member.cooperative)
                    __member.save()
                    return Response(
                        {"status": "OK", "response": "Farmer Profile Saved Successfully"},
                        status.HTTP_200_OK)
            return Response(member.errors)
        except Exception as err:
            return Response({"status": "ERROR", "response": err}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(member.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        cooperative = request.data.get('cooperative')  
        # members = CooperativeMember.objects.filter(cooperative=request.user.cooperative_admin.cooperative).order_by('-surname')
        members = CooperativeMember.objects.filter(cooperative=cooperative).order_by('-surname')
        if member:
            members = members.filter(Q(member_id=member)|Q(phone_number=member)|Q(other_phone_number=member))
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    

class TrainingSessionView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        pk = request.data.get('session_id')
        print pk
        training = TrainingSessionSerializer(data=request.data)
        
        try:
            if pk:
                ts = TrainingSession.objects.get(pk=pk)
                print ts
                training = TrainingSessionUpdateSerializer(ts, data=request.data)
            print request.data
            if training.is_valid():
                print training
                with transaction.atomic():
                    ta = request.data.get('thematic_area')
                    tq = ThematicArea.objects.filter(pk=ta)
                    __training = training.save(thematic_area=tq[0])
                    __training.trainer = request.user
                    __training.created_by = request.user
                    if not pk:
                        __training.training_reference = generate_alpanumeric(prefix="TR", size=8)
                    __training.save()
                    
                    #get Member list
                    data = request.data
                    if pk:
                        __training.coop_member.clear()
                    for m in data.get('member'):
                        member = CooperativeMember.objects.get(member_id=m)
                        __training.coop_member.add(member)
                    
                    return Response(
                        {"status": "OK", "response": "Training Session Saved"},
                        status.HTTP_200_OK)
            
            return Response(training.errors)
        except Exception as err:
            log_error()
            return Response({"status": "ERRORf", "response": err}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(training.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TrainingSessionListView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        cooperative = request.data.get('cooperative')
        print "Cooperative" + cooperative
        training = TrainingSession.objects.filter(cooperative=cooperative).order_by('-create_date')
        # training = TrainingSession.objects.all().order_by('-create_date')
        serializer = TrainingSessionSerializer(training, many=True)
        return Response(serializer.data)
    

class TrainingSessionEditView(APIView): #DRY thrown out here. Need fix
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, session, format=None):
        cooperative = request.data.get('cooperative')
        print "Cooperative" + cooperative
        training = TrainingSession.objects.filter(cooperative=cooperative, pk=session).order_by('-create_date')
        # training = TrainingSession.objects.all().order_by('-create_date')
        serializer = TrainingSessionEditSerializer(training, many=True)
        return Response(serializer.data)
    
    
class CollectionCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        collection = CollectionSerializer(data=request.data)
        if collection.is_valid():
            try:
                with transaction.atomic():
                    c = collection.save(created_by = request.user)
                    # collection_date = data.get('collection_date')
                    # is_member = data.get('is_member')
                    # member = data.get('member')
                    # name = data.get('name')
                    # phone_number = data.get('phone_number')
                    # collection_reference = data.get('collection_reference')
                    # product = data.get('product')
                    # quantity = data.get('quantity')
                    # unit_price = data.get('unit_price')
                    # total_price = data.get('total_price')
                    # created_by = data.get('created_by')
                    if c.is_member:
                        params = {
                            'amount': c.total_price,
                            'member': c.member,
                            'transaction_reference': c.collection_reference ,
                            'transaction_type': 'COLLECTION',
                            'entry_type': 'CREDIT'
                        }
                        member = CooperativeMember.objects.filter(pk=c.member.id)
                        if member.exists():
                            member = member[0]
                            qty_bal = member.collection_quantity if member.collection_quantity else 0
                            new_bal = c.quantity + qty_bal
                            member.collection_quantity = new_bal
                            member.save()
                        save_transaction(params)
                        try:
                            message = message_template().collection
                            message = message.replace('<NAME>', member.surname)
                            message = message.replace('<QTY>', "%s%s" % (c.quantity, c.product.unit.code))
                            message = message.replace('<PRODUCT>', "%s" % (c.product.name))
                            message = message.replace('<COOP>', c.cooperative.name)
                            message = message.replace('<DATE>', c.collection_date.strftime('%Y-%m-%d'))
                            message = message.replace('<AMOUNT>', "%s" % c.total_price)
                            message = message.replace('<REFNO>', c.collection_reference)
                            sendMemberSMS(self.request, member, message)
                        except Exception:
                            log_error()

                    return Response(
                                {"status": "OK", "response": "Collection Saved."},
                                status.HTTP_200_OK)
            except Exception as e:
                log_error()
                return Response({"status": "ERROR", "response": "error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(collection.errors)
            

class CollectionListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        #raise Exception(request.user)
        cooperative = request.data.get('cooperative')
        collections = Collection.objects.filter(cooperative=cooperative).order_by('-create_date')
        serializer = CollectionListSerializer(collections, many=True)
        return Response(serializer.data)
    

class MemberOrderListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        cooperative = request.data.get('cooperative')
        orders = MemberOrder.objects.filter(cooperative=cooperative).order_by('-create_date')
        serializer = MemberOrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderItemListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, order, format=None):
        order_items = OrderItem.objects.filter(order=order).order_by('-create_date')
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)


class ItemView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    
class OrderCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        data = request.data 
        mo = MemberOrderFormSerializer(data=data)
        if mo.is_valid():
            _order = mo.save(created_by=request.user)
            for i in data.get("item"):
                oi = OrderItemSerializer_(data=i)
                if oi.is_valid():
                    oi.save(order=_order, created_by=request.user)
                else:
                    return Response(oi.errors)
            return Response({"status": "OK", "response": "Order Saved"}, status.HTTP_200_OK)
        return Response(mo.errors)


