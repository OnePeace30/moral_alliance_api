import json
import math
import requests
import logging
from datetime import datetime as dt, timedelta

from models import (State, Universities, RelatedArticles, HateGroups, Gifts,
                    SMPosts, AlumniNotable, EventsAnnotated, Events)
from util import Database
from annotated_tables import regenerate_gifts, regenerate_events
from serializers_schema import (
    StateSerializer, UniversitiesSerializer, RelatedArticlesSerializer,
    HateGroupsSerializer, GiftsSerializer, SMPostsSerializer, AlumniNotableSeralizer,
    EventsAnnotatedSerializer, EventsSerializer)
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("moral_alliance")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('moral_alliance.log', interval=1, backupCount=3, when='d')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

meta_posts = {"posts": 
                {
                    "model": SMPosts, 
                    "serializer": SMPostsSerializer, 
                    "how": "filter", 
                    "order": SMPosts.score.asc(), 
                    "limit": 3, 
                    "filters": [
                        SMPosts.post_create.between(dt.now() - timedelta(days=61), dt.now()),
                    ]
                }
            }

all_points = {
    'states': {"model": State, "serializer": StateSerializer, "how": "all"},
    'universities': {"model": Universities, "serializer": UniversitiesSerializer, "how": "all"},
    # 'articles': {"model": RelatedArticles, "serializer": RelatedArticlesSerializer, "how": "all", "order": RelatedArticles.date.desc()},
    'groups': {"model": HateGroups, "serializer": HateGroupsSerializer, "how": "all"},
    'gifts': {"model": Gifts, "serializer": GiftsSerializer, "how": "all", "filters": [Gifts.university_id.isnot(None)]},
    'alumni': {"model": AlumniNotable, "serializer": AlumniNotableSeralizer, "how": "all"},
    'incidents': {"model": EventsAnnotated, "serializer": EventsAnnotatedSerializer, "how": "all"},
    'feed': {"model": Events, "serializer": EventsSerializer, "how": "all", "filters": [Events.uni_id.isnot(None)]}
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


def main(point, args, filters = []):
    if point == 'gifts':
        to_delete = regenerate_gifts()
        api('delete_gifts', to_delete)
    elif point == 'events':
        regenerate_events()
    if args['how'] == 'all':
        objs = db.session.query(args['model'])
        if args.get('filters'):
            for filter in args.get('filters'):
                objs = objs.filter(filter)
        objs = objs.all()
        data = [args['serializer'](o).data for o in objs]
        # logger.info("DATA")
        # logger.info(data)
        print()
    elif args['how'] == 'limit':
        objs = db.session.query(args['model']).order_by(args['order']).limit(args['limit'])
        data = [args['serializer'](o).data for o in objs]
        print()
    elif args['how'] == 'filter':
        objs = db.session.query(args['model']).filter(args['filter']).order_by(args['order']).limit(args['limit'])
        data = [args['serializer'](o).data for o in objs]
        print()
    api(point, data)
    # if point == "universities":
    #     for obj in objs:
    #         meta = db.session.query(SMPosts).filter(SMPosts.post_create.between(dt.now() - timedelta(days=61), dt.now()))\
    #                 .filter(SMPosts.uni_id == obj.id).order_by(SMPosts.score.asc()).limit(3)
    #         data = [SMPostsSerializer(o).data for o in meta]
    #         api('posts', data)


def api(point, data):
    ma = MoralAlliance()
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


if __name__ == '__main__':
    db = Database()
    for point, args in all_points.items():
        main(point, args)
    # data = [i for i in range(1, 20000)]
    # api('delete_posts', data)