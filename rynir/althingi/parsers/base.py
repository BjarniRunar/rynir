import hashlib
import os
import re
import urllib2

import settings


class ScraperParser:
  MATCH_URLS = ( )

  scrape_and_parse = None

  def urls(self, url):
    urldir = url
    if not urldir.endswith('/'):
      urldir = urldir.rsplit('/', 1)[0] + '/'
    urlbase = '/'.join(url.split('/')[:3]) + '/'
    return urlbase, urldir

  def extract_urls(self, url, soup):
    urlbase, urldir = self.urls(url)
    urls = {}
    for result in soup.fetch('a'):
      href = result.get('href')
      if href:
        if href.startswith('/'):
          href = urlbase+href[1:]
        urls[href] = 1
    return urls.keys()

  def scrape(self, url, ignore_cache=False):
    #print 'Scraping: %s' % url
    cache_id = hashlib.md5(url).hexdigest()[:20]
    cache_fn = os.path.join(settings.RYNIR_SCRAPE_PATH, cache_id)
    try:
      if ignore_cache or not os.path.exists(cache_fn):
        data = urllib2.urlopen(url).read()
        fd = open(cache_fn, 'wb')
        fd.write(data)
        fd.close()
      return (cache_id, open(cache_fn, 'rb').read())
    except (OSError, IOError):
      return (cache_id, None)

  def parse(self, url, data, fromEncoding=None):
    return None


