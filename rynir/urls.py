from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Content
    (r'^/?$',                                     'althingi.views.index'),
    (r'^static/(.*)$',                            'althingi.views.static'),
    (r'^thingmenn/?$',                            'althingi.views.thingmenn'),
    (r'^thingmenn/(?P<althingi_id>[^/]+)/?$',     'althingi.views.thingmadur'),
    (r'^kosningar/?$',                            'althingi.views.kosningar'),
    (r'^kosningar/(?P<kosning_uid>.+?)/?$',       'althingi.views.kosning'),

    # Scraper
    (r'^scrape/(?P<proto>https?)(?::/)?/(?P<domain>[^/]+)/(?P<path>.*)$',
                                                  'althingi.scraper.scrape'),
    (r'^scrape/bootstrap(?P<testing>/testing)?$', 'althingi.scraper.bootstrap'),
    (r'^scrape/bootstrap/(?P<fundir>[\d,]+)/?$',  'althingi.scraper.bootstrap'),

    # The admin
    (r'^admin/', include(admin.site.urls)),
)
