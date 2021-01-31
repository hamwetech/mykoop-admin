# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
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
from conf.models import District, County, SubCounty, Village
from supplier.models import Supplier, Item, OrderItem
from system.models import Union, CooperativeMember
from apiv1.serializers import *

from django.shortcuts import render


class SupplierListView(APIView):
    pass


class ItemsListView(APIView):
    def post(self, request, member=None, format=None):
        suppliers = Supplier.objects.all()
        payload = dict()
        ar = []
        for s in suppliers:
            payload.update({'supplier': s.name})
            items = Item.objects.filter(supplier=s)

            for i in items:
                ar.append({'item':i.name, 'price':i.price})
            payload.update(ar)
        return Response(payload)


class SaveMember(APIView):
    def post(self, request, member=None, format=None):
        data = request.data

        try:
            member = MemberSerializer(data=request.data)
            if member.is_valid():
                union = data.get('union')

                if union:
                    unions = Union.objects.filter(name__icontains=union)
                    print(unions[0].name.lower())
                    if unions.exists():
                        with transaction.atomic():
                            if union.lower() == unions[0].name.lower():
                                __member = member.save(using=unions[0].name.lower())
                                __member.member_id = self.generate_member_id(__member.cooperative)
                                # __member.create_by = request.user
                                __member.save(using=unions[0].name.lower())
                            return Response(
                                {"status": "OK", "response": "Member Profile Saved Successfully",
                                 "member_id": __member.member_id},
                                    status.HTTP_200_OK)
                    return Response({"status": "FAILED", "response": "Union not found"})
                return Response({"status": "FAILED", "response": "Union is missing"})
            return Response({"status": "FAILED", "response": member.errors})
        except Exception as err:
            return Response({"status": "FAILED", "response": err}, status.HTTP_200_OK)

class MemberListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, member=None, format=None):
        member = CooperativeMember.objects.all()
        serializer = MemberSerializer(cooperatives, many=True)
        return Response(serializer.data)
