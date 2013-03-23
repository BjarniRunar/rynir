import re
from htmlparser import ScraperParserHTML
from metaparser import RegisterScraperParser


SATUHJA_RE = re.compile('\(([^\)]+)\) greiddu ekki')
FJARSTADDIR_RE = re.compile('\(([^\)]+)\) fjarstaddir')


class ScraperParserFundarmal(ScraperParserHTML):
  MATCH_URLS = ('http://www.althingi.is/altext/\d+/\d+/l\d+\.sgml$', )
  SCRAPE_URLS = ( )

  def parse(self, url, data):
    soup = ScraperParserHTML.parse(self, url, data)

    efni = soup.h2

    for para in soup.fetch('p'):
      brtt = para.a
      vote = para.dl
      if brtt is None and vote:
        elem = vote.next
        svar = None
        ja, nei, fj, sh = [], [], [], []
        while elem:
          name = getattr(elem, 'name', None)

          if name == 'dt':
            svar = elem.b.string.replace('&nbsp;', '').strip()[:-1]

          elif name == 'dd':
            folk = elem.string.replace('.', '').strip().split(', ')
            if svar.startswith('j'):
              ja = folk
            elif svar.startswith('n'):
              nei = folk

          elif name == 'p':
            satuhja = SATUHJA_RE.search(elem.string or '')
            fjarstaddir = FJARSTADDIR_RE.search(elem.string or '')
            if satuhja:
              sh = satuhja.group(1).replace('.', '').strip().split(', ')
            elif fjarstaddir:
              fj = fjarstaddir.group(1).replace('.', '').strip().split(', ')

            if not (elem.string and elem.string.strip()): break

          elem = elem.next

        # FIXME: Create Umraeda/Kosning/Atkvaedi objects in DB
        print 'J: %s' % ja
        print 'N: %s' % nei
        print 'F: %s' % fj
        print 'S: %s' % sh

    return True

RegisterScraperParser(ScraperParserFundarmal)
