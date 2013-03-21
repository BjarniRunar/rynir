import re

from base import ScraperParser


SCRAPER_PARSERS = { }

def Register(cls):
  for rxp in cls.MATCH_URLS:
    SCRAPER_PARSERS[re.compile(rxp)] = cls


class MetaParser(ScraperParser):

  def _scrape_and_parse(self, url):
    scrape_id, data = self.scrape(url)
    if scrape_id:
      return self.parse(url, data)
    else:
      return None

  scrape_and_parse = _scrape_and_parse

  def parse(self, url, data):
    rv = None
    for rxp, cls in SCRAPER_PARSERS.iteritems():
      if rxp.match(url):
        print 'Routing %s to %s' % (url, cls)
        sp = cls()
        sp.scrape_and_parse = self.scrape_and_parse
        rv = sp.parse(url, data) and rv
    if not rv:
      print 'No route for %s' % url
    return rv

