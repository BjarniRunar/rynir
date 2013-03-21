from htmlparser import ScraperParserHTML
from metaparser import Register

class ScraperParserFundur(ScraperParserHTML):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/f\d+\.sgml$', )
  SCRAPE_URLS = ('http://www.althingi.is/altext/\d+/\d+/l\d+\.sgml$', )

Register(ScraperParserFundur)
