from django.conf.urls import url
from . import views

urlpatterns = [
	# url(r'index/$', views.home, name='home'),
	url(r'index/$', views.Home.as_view(), name='home'),
	# url(r'detail/(?P<sku_id>\d+)$', views.detail, name='detail'),
	url(r'detail/(?P<sku_id>\d+)$', views.Detail.as_view(), name='detail'),
	# url(r'list/(?P<type>\d+)/(?P<page_num>\d+)/$', views.list, name='list'),
	url(r'list/(?P<type>\d+)/(?P<page_num>\d+)/$', views.List.as_view(), name='list'),
	# url(r'$', views.home, name='home'),
]
