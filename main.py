import json
import requests
import logging

from models import State, Universities, RelatedArticles, HateGroups
from util import Database
from serializers_schema import (
    StateSerializer, UniversitiesSerializer, RelatedArticlesSerializer,
    HateGroupsSerializer)
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
    'articles': {"model": RelatedArticles, "serializer": RelatedArticlesSerializer, "how": "limit", "limit": 100, "order": RelatedArticles.date.desc()},
    'groups': {"model": HateGroups, "serializer": HateGroupsSerializer, "how": "all"}
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
            objs = db.session.query(args['model']).all()
            data = [args['serializer'](o).data for o in objs]
            print()
        elif args['how'] == 'limit':
            objs = db.session.query(args['model']).order_by(args['order']).limit(args['limit'])
            data = [args['serializer'](o).data for o in objs]
            print()
        r = ma.request(point, data)
        if r.status_code == 200:
            logger.info(f"Sended {len(data)} to {point} ")
            logger.info(r.json())
        else:
            logger.error(f"Error send {len(data)} to {point}")
            logger.info(r.json())