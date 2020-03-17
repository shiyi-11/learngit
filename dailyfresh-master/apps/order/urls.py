from django.conf.urls import url
from . import views
# 主url中没有应用，次url中就要填上app_name=‘应用名’
app_name = 'order'
urlpatterns = [
    # url(r'^commit/$', views.create_order, name='corder'),
    url(r'^commit/$', views.Create_order.as_view(), name='corder'),
    url(r'^payorder/$', views.payorder, name='payorder'),
    url(r'^orderpay/$', views.orderpay, name='orderpay'),
    url(r'^checkorder/$', views.checkorder, name='checkorder'),
]
