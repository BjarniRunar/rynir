from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^rynir/', include('rynir.foo.urls')),
    (r'^/?$',                                        'althingi.views.index'),
    (r'^fundur/(?P<fundur_id>\d+)/$',                'althingi.views.fundur'),
    (r'^scrape/(?P<proto>https?)/(?P<domain>[^/]+)/(?P<path>.*)$',
                                                     'althingi.views.scrape'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
