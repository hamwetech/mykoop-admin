from django.conf.urls import url, include
from rest_framework import routers
from apiv1.views import *


router = routers.DefaultRouter()

urlpatterns = [
    url('', include(router.urls)),
    url(r'items/list/$', ItemsListView.as_view(), name='item_list'),
    url(r'items/list/(?P<order>[-\w]+)/$', ItemsListView.as_view(), name='item_list'),

    url(r'member/create/$', SaveMember.as_view(), name='create_member'),
    url(r'member/list/$', MemberListView.as_view(), name='member_list'),
 ]