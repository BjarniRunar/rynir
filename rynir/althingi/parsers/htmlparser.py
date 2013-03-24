import re

from base import ScraperParser

import chardet # Dummy import, BeautifulSoup uses this
from BeautifulSoup import BeautifulSoup

class ScraperParserHTML(ScraperParser):
  SCRAPE_URLS = ( )

  def parse(self, url, data, soup=None, fromEncoding=None):
    soup = soup or BeautifulSoup(data, fromEncoding=fromEncoding)
    if self.scrape_and_parse and self.SCRAPE_URLS:
      scrape = {}
      for url in self.extract_urls(url, soup):
        for rxp in self.SCRAPE_URLS:
          if re.compile(rxp).match(url):
            scrape[url] = 1
      for url in scrape.keys():
        self.scrape_and_parse(url)
    return soup
