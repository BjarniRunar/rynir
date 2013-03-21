import re

from base import ScraperParser
from metaparser import Register

import chardet # Dummy import, BeautifulSoup uses this
from BeautifulSoup import BeautifulSoup

class ScraperParserHTML(ScraperParser):
  SCRAPE_URLS = ( )

  def parse(self, url, data):
    soup = BeautifulSoup(data)
    if self.scrape_and_parse:
      scrape = {}
      for url in self.extract_urls(url, soup):
        for rxp in self.SCRAPE_URLS:
          if re.compile(rxp).match(url):
            scrape[url] = 1
      for url in scrape.keys():
        self.scrape_and_parse(url)
    return soup
