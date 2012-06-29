from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from shop.models import *

admin.autodiscover()

urlpatterns = patterns('Shop',
    # Examples:
    # url(r'^$', 'Shop.views.home', name='home'),
    # url(r'^Shop/', include('Shop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     (r'^grappelli/', include('Shop.grappelli.urls')),
     (r'^porduct/$', 'shop.views.product_list',) , 
     (r'^$', 'shop.views.index',) , 
     
     (r'^product/(?P<slug>[-\w]+)/$', 'shop.views.product_details', ), 
    url(r'^cart/add/(?P<slug>[-\w]+)/$', 'shop.views.add_to_cart',{'queryset': Product.objects.all()},name='cart_add_product'),
    url(r'^cart/$', 'shop.views.shopping_cart', {},name='orders_cart'),
     #(r'^accounts/', include('registration.backends.default.urls'))
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

