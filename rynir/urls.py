from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Content
    (r'^/?$',                                     'althingi.views.index'),
    (r'^static/(.*)$',                            'althingi.views.static'),
    (r'^thingmenn/(?P<thingmadur_id>[^/]+)?/?$',  'althingi.views.thingmenn'),
    (r'^kosningar/(?P<kosning_uid>[^/]+)?/?$',    'althingi.views.kosningar'),

    # Scraper
    (r'^scrape/(?P<proto>https?)(?::/)?/(?P<domain>[^/]+)/(?P<path>.*)$',
                                                  'althingi.scraper.scrape'),
    (r'^scrape/bootstrap$',                       'althingi.scraper.bootstrap'),

    # The admin
    (r'^admin/', include(admin.site.urls)),
)
