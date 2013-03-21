from htmlparser import ScraperParserHTML
from metaparser import Register

import chardet # Dummy import, BeautifulSoup uses this
from BeautifulSoup import BeautifulSoup

class ScraperParserFundur(ScraperParserHTML):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/f\d+\.sgml$', )
  SCRAPE_URLS = ('http://www.althingi.is/altext/\d+/\d+/l\d+\.sgml$', )

Register(ScraperParserFundur)
