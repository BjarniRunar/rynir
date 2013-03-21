from base import ScraperParser
from metaparser import Register

class ScraperParserFundur(ScraperParser):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/f\d+\.sgml$', )
 
Register(ScraperParserFundur)
