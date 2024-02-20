import requests
import pandas as pd

from xml.etree import ElementTree as ET


class Base():

    def __init__(self):
        self._link = None
        self.items = []
        self.namespaces = {}

    @property
    def link(self):
        if self._link is None:
            raise AssertionError("The link is not defineded")
        return self._link

    @link.setter
    def link(self, link):
        assert isinstance(link, str)
        self._link = link

    def get_content(self):
        response = requests.get(self.link)
        return response.text

    def parce(self):
        content = self.get_content()
        root = ET.fromstring(content)
        self._parce(root)

    def _parce(self, root:ET):
        print()


class Cnnrss(Base):

    def __init__(self):
        super().__init__()
        self.namespaces = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "content": "http://purl.org/rss/1.0/modules/content/",
            "atom": "http://www.w3.org/2005/Atom",
            "media": "http://search.yahoo.com/mrss/"
        }

    def _parce(self, root:ET):
        channel = root.find('channel')
        items = channel.findall('item')
        for item in items:
            o = {}
            o["title"] = item.find('title').text
            o["link"] = item.find('link').text
            try:
                o["text"] = item.find('description').text
            except AttributeError:
                o["text"] = None
            try:
                o["pic"] = item.find('media:group', self.namespaces).findall('media:content', self.namespaces)[0].attrib['url']
            except AttributeError:
                o['pic'] = None
            try:
                o["date"] = pd.to_datetime(item.find('pubDate').text)
            except AttributeError:
                o["date"] = None
            self.items.append(o)


class Nytrss(Base):

    def __init__(self):
        super().__init__()
        self.namespaces = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "nyt": "http://www.nytimes.com/namespaces/rss/2.0",
            "atom": "http://www.w3.org/2005/Atom",
            "media": "http://search.yahoo.com/mrss/"
        }

    def _parce(self, root:ET):
        channel = root.find('channel')
        items = channel.findall('item')
        for item in items:
            o = {}
            o["title"] = item.find('title').text
            o["link"] = item.find('link').text
            try:
                o["text"] = item.find('description').text
            except AttributeError:
                o["text"] = None
            try:
                o["pic"] = item.find('media:content', self.namespaces).attrib['url']
            except AttributeError:
                o['pic'] = None
                continue
            try:
                o["date"] = pd.to_datetime(item.find('pubDate').text)
            except AttributeError:
                o["date"] = None
            self.items.append(o)