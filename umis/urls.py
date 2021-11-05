"""umis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from conf import urls as conf_urls
from supplier import urls as supplier_url
from userprofile import urls as profile_urls
from apiv1 import urls as api_urls
from system.views import CooperativesListView, UnionListView, UnionCreateView, UnionUpdateView, MembersListView, AgentListView, MembersOrderListView, UnionDeleteView


from dashboard.views import DashboardView
from userprofile.views.authentication import LoginView, LogoutView
from conf.views import Handle404, Handle403

handler404 = Handle404.as_view()
handler403 = Handle403.as_view()

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^conf/', include(conf_urls, namespace='conf')),
    url(r'^supplier/', include(supplier_url, namespace='supplier')),
    url(r'^profile/', include(profile_urls, namespace='profile')),
    url(r'^apiv1/', include(api_urls, namespace='api')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^union/$', UnionListView.as_view(), name='union_list'),
    url(r'^union/create/$', UnionCreateView.as_view(), name='union_create'),
    url(r'^union/create/(?P<pk>[\w]+)/$', UnionUpdateView.as_view(), name='union_update'),
    url(r'^union/delete/(?P<pk>[\w]+)/$', UnionDeleteView.as_view(), name='union_delete'),
    url(r'^cooperative/$', CooperativesListView.as_view(), name='cooperative_list'),
    url(r'^member/$', MembersListView.as_view(), name='member_list'),
    url(r'^agent/$', AgentListView.as_view(), name='agent_list'),
    url(r'^orders/$', MembersOrderListView.as_view(), name='order_list'),
    url(r'^$', DashboardView.as_view(), name='dashboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
