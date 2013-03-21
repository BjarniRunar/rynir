from . import metaparser

class ScraperParserFundur(metaparser.ScraperParser):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/f\d+\.sgml$', )
 
metaparser.Register(ScraperParserFundur)
