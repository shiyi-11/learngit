from django.conf.urls import url, include
from django.contrib import admin
# from apps.product.views import home, Home
from apps.product.views import Home
from django.views.static import serve
from . import settings
from tests import views




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    # url(r'^tinymce', include('tinymce.urls')),
    url(r'^search/', include('haystack.urls')),

    # url(r'^user/', include('user.urls', namespace='user')),
    url(r'^user/', include(('apps.user.urls','user'), namespace='user')),

    # url(r'^order/', include('order.urls', namespace='order')),
    # url(r'^cart/', include('cart.urls', namespace='cart')),
    # url(r'^product/', include('product.urls', namespace='product')),
    url(r'^order/', include(('apps.order.urls', 'order'), namespace='order')),
    url(r'^cart/', include(('apps.cart.urls', 'cart'), namespace='cart')),

    # url命名空间namespace是对应特定的应用，能对应唯一的url
    # 而name相等于给url起名字，如果同一项目的url名字有重复，就会出现一个views或一个templates对应多个url
    url(r'^test$',views.test),
    url(r'^product/', include(('apps.product.urls', 'product')), name='product'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # url(r'^$', home, name='home'),
    url(r'^$', Home.as_view(),name='home')
]
