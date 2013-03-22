from htmlparser import ScraperParserHTML
from metaparser import RegisterScraperParser

class ScraperParserFundarmal(ScraperParserHTML):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/\d+/l\d+\.sgml$', )
  SCRAPE_URLS = ( )

  def parse(self, url, data):
    soup = ScraperParserHTML.parse(self, url, data)

    efni = soup.h2

    for para in soup.fetch('p'):
      mal = para.a
      for vote in para.fetch('dl'):
        svar = vote.dt
        menn = vote.dd
        print '%s said %s about %s' % (menn, svar, mal)

    return True

RegisterScraperParser(ScraperParserFundarmal)
