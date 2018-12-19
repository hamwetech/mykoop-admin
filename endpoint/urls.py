from django.conf.urls import url
from endpoint.views import MemberEndpoint, Login, MemberList, TrainingSessionListView,TrainingSessionView

urlpatterns = [
    url(r'training/create/$', TrainingSessionView.as_view(), name='training_create'),
    url(r'member/list/(?P<member>[-\w\s]+)/$', MemberList.as_view(), name='member_list'),
    url(r'member/list/$', MemberList.as_view(), name='member_list'),
    url(r'member/register/$', MemberEndpoint.as_view(), name='member_create'),
    url(r'login/$', Login.as_view(), name='login'),
 ]