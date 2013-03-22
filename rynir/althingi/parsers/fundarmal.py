from htmlparser import ScraperParserHTML
from metaparser import RegisterScraperParser

class ScraperParserFundarmal(ScraperParserHTML):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/\d+/l\d+\.sgml$', )
  SCRAPE_URLS = ( )

  def parse(self, url, data):
    return True

RegisterScraperParser(ScraperParserFundarmal)
