import logging

import pandas as pd
import requests
from xml.etree import ElementTree as ET

from util import MLStripper

logger = logging.getLogger('gnews')


class GoogleRSS:

    def __init__(self):
        logger.info('Start new process')
        self.link = "https://news.google.com/rss/search"
        self.items = []
        self.kw = None

    def start(self)->None:
        for kw in self.keywords:
            self.kw = kw
            logger.info(f'start process for {kw}')

    def get_content(self, kw)->None:
        params = {
            'q': f"{kw} when:5d",
            'hl': 'en'
        }
        response = requests.get(self.link, params=params)
        return response.text
    

    def null_value(self,value):
        return value if value else None

    def parce (self, xml:str):
        # soup = BeautifulSoup(xml, 'xml')
        # self.items = soup.findAll('item')
        root = ET.fromstring(xml)
        c = root.find('channel')
        return c.findall('item')


    def get_data(self, kw):
        content = self.get_content(kw)
        items = self.parce(content)
        for item in items:
            yield {
                "title": item.find('title').text,
                "link": item.find('link').text,
                "text": self.strip_tags(item.find('description').text),
                "date": pd.to_datetime(item.find('pubDate').text),
            }

    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

