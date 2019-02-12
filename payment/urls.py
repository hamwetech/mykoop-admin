from django.conf.urls import url

from payment.views import *

urlpatterns = [
    
    url(r'edit/(?P<pk>[\w]+)/$', PaymentMethodUpateView.as_view(), name='update'),
    url(r'dowload/$', DownloadPaymentExcelView.as_view(), name='download'),
    url(r'list/$', PaymentMethodListView.as_view(), name='list'),
    url(r'create/$', PaymentMethodCreateView.as_view(), name='create')
]

