import json
import math
import requests
import logging
from datetime import datetime as dt, timedelta

from models import (State, Universities, RelatedArticles, HateGroups, Gifts,
                    SMPosts)
from util import Database
from serializers_schema import (
    StateSerializer, UniversitiesSerializer, RelatedArticlesSerializer,
    HateGroupsSerializer, GiftsSerializer, SMPostsSerializer)
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("moral_alliance")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('moral_alliance.log', interval=1, backupCount=3, when='d')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

all_points = {
    'states': {"model": State, "serializer": StateSerializer, "how": "all"},
    'universities': {"model": Universities, "serializer": UniversitiesSerializer, "how": "all"},
    'articles': {"model": RelatedArticles, "serializer": RelatedArticlesSerializer, "how": "all", "filters": [RelatedArticles.date >= dt.now() - timedelta(days=1)], "order": RelatedArticles.date.desc()},
    'groups': {"model": HateGroups, "serializer": HateGroupsSerializer, "how": "all"},
    'gifts': {"model": Gifts, "serializer": GiftsSerializer, "how": "all", "filters": [Gifts.university_id.isnot(None)]},
    'posts': {"model": SMPosts, "serializer": SMPostsSerializer, "how": "filter", "order": SMPosts.score.asc(), "limit": 3, "filter": SMPosts.post_create.between(dt.now() - timedelta(days=61), dt.now())},
}


class MoralAlliance(object):
    BASE_URL = "https://www.moral-alliance.com/_functions/"
    PostMethod = 'POST'
    GetMethod = 'GET'

    def __init__(self):
        self.base_method = MoralAlliance.PostMethod

    def request(self, point, payload, method=None):
        if method is None:
            m = self.base_method
        else:
            m = method
        url = self.BASE_URL + point
        response = requests.request(m, url, data=json.dumps(payload))
        return response


if __name__ == '__main__':
    db = Database()
    # p = db.session.query(State).all()
    # # print(p[0].to_dict(rules=['-articles']))
    # slz = StateSerializer(p[0])
    # slz.serialize()
    # print(slz.data)
    for point, args in all_points.items():
        ma = MoralAlliance()
        if args['how'] == 'all':
            objs = db.session.query(args['model'])
            if args.get('filters'):
                for filter in args.get('filters'):
                    objs = objs.filter(filter)
            data = [args['serializer'](o).data for o in objs]
            print()
        elif args['how'] == 'limit':
            objs = db.session.query(args['model']).order_by(args['order']).limit(args['limit'])
            data = [args['serializer'](o).data for o in objs]
            print()
        elif args['how'] == 'filter':
            objs = db.session.query(args['model']).filter(args['filter']).order_by(args['order']).limit(args['limit'])
            data = [args['serializer'](o).data for o in objs]
            print()
        pages = math.ceil(len(data)/1000)
        for page in range(0, pages):
            d = data[page*1000: page*1000 + 1000]
            r = ma.request(point, d)
            if r.status_code == 200:
                logger.info(f"Sended {len(d)} to {point} ")
                logger.info(r.json())
            else:
                logger.error(f"Error send {len(d)} to {point}")
                logger.info(r.json())