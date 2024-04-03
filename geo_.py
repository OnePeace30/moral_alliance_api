import json
import math
import logging

from geopy.distance import geodesic as GD 

from models import (State, Universities, RelatedArticles, HateGroups, Gifts,
                    SMPosts, AlumniNotable, Events)
from util import Database
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("moral_alliance_geo")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('moral_alliance_geo.log', interval=1, backupCount=3, when='d')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__':
    db = Database()
    events = db.session.query(Events).filter(Events.uni_id == None)
    universities = db.session.query(Universities).all()
    for event in events:
        print(event.id)
        dist = 40000
        if event.lng is None: continue
        point = (event.lat, event.lng)
        nearest_uni = None
        for uni in universities:
            if uni.lng is None: continue
            uni_point = (uni.lat, uni.lng)
            distance = GD(point, uni_point)
            if distance < dist:
                dist = distance
                nearest_uni = uni.id
        print(event.id, nearest_uni, dist, sep=' - ')
        event.uni_id = nearest_uni
        db.session.commit()

