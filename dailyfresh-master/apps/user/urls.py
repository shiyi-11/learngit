from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    url(r'^register/checkname/(?P<name>\w+)$', views.check_name, name='checkname'),
    url(r'^register/active/(?P<token>.*)$', views.active_acount, name='active'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^login/$', views.Tt_login.as_view(), name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^userinfo/$', views.User_info.as_view(), name='userinfo'),
    # url(r'^userorder/(\w+)$', views.user_order, name='userorder'),
    url(r'^userorder/(\w+)$', login_required(views.User_order.as_view()), name='userorder'),
    # url(r'^userorder/$', login_required(views.User_order.as_view()), name='userorder'),
    # url(r'^useraddress', views.useraddress, name='useraddress'),
    url(r'^address', login_required(views.Useraddress.as_view()), name='address'),
    url(r'^address', login_required(views.Useraddress.as_view()), name='useraddress'),


]
