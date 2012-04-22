from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),
    (r'^cal/?$','mysite.cal.views.index'),
    (r'^cal/(?P<pYear>\d{4})/(?P<pMonth>\d{1,2})/?$','mysite.cal.views.calendar'),

                       
    (r'^cal/(?P<user_name>[a-zA-Z0-9_]+)/?$','mysite.cal.views.index_user'),
    (r'^cal/(?P<pYear>\d{4})/(?P<pMonth>\d{1,2})/(?P<user_name>[a-zA-Z0-9_]+)/?$','mysite.cal.views.calendar_user'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
