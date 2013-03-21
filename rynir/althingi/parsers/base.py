import hashlib
import os
import re
import urllib2

import settings


class ScraperParser:
  MATCH_URLS = ( )

  def scrape(self, url, ignore_cache=False):
    cache_id = hashlib.md5(url).hexdigest()[:20]
    cache_fn = os.path.join(settings.RYNIR_SCRAPE_PATH, cache_id)
    try:
      if ignore_cache or not os.path.exists(cache_fn):
        data = urllib2.urlopen(url).read()
        open(cache_fn, 'wb').write(data)
      return (cache_id, open(cache_fn, 'rb').read())
    except (OSError, IOError):
      return (cache_id, None)

  def parse(self, url, data):
    return None

