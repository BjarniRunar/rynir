import re

from althingi.models import *
from htmlparser import ScraperParserHTML
from metaparser import RegisterScraperParser

import chardet # Dummy import, BeautifulSoup uses this
from BeautifulSoup import BeautifulSoup


DATE_RE = re.compile(' (\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d) (\\d\\d?):(\\d\\d), ')

class ScraperParserFundur(ScraperParserHTML):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/f\d+\.sgml$', )
  SCRAPE_URLS = ('http://www.althingi.is/altext/\d+/\d+/l\d+\.sgml$', )

  def parse(self, url, data):
    soup = BeautifulSoup(data)

    title = soup.fetch('title')[0].string
    nr = soup.fetch('h1')[0].string.split('.', 1)[0]

    m = DATE_RE.search(title)
    year = int(m.group(1))
    mon = int(m.group(2))
    day = int(m.group(3))
    hour = int(m.group(4))
    minu = int(m.group(5))

    existing = Fundur.objects.filter(nr=nr)
    if existing:
      fn = existing[0]
    else:
      fn = Fundur()

    fn.titill = title
    fn.dags = '%4.4d-%2.2d-%2.2d %2.2d:%2.2d' % (year, mon, day, hour, minu)
    fn.save()

    return ScraperParserHTML.parse(self, url, data, soup=soup)

RegisterScraperParser(ScraperParserFundur)
