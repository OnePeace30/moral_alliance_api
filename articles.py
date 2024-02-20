from rss import Cnnrss, Nytrss

import logging
from logging.handlers import TimedRotatingFileHandler

from util import Database
from models import Universities, RelatedArticles

logger = logging.getLogger("rss")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(f"rss.log", interval=1, backupCount=3, when='d')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)


links = {
    Cnnrss: [
        "http://rss.cnn.com/rss/edition.rss",
        "http://rss.cnn.com/rss/edition_world.rss",
        "http://rss.cnn.com/rss/edition_africa.rss",
        "http://rss.cnn.com/rss/edition_americas.rss",
        "http://rss.cnn.com/rss/edition_asia.rss",
        "http://rss.cnn.com/rss/edition_europe.rss",
        "http://rss.cnn.com/rss/edition_meast.rss",
        "http://rss.cnn.com/rss/edition_us.rss",
        "http://rss.cnn.com/rss/money_news_international.rss",
        "http://rss.cnn.com/rss/edition_technology.rss",
        "http://rss.cnn.com/rss/cnn_latest.rss",
        "http://rss.cnn.com/rss/cnn_freevideo.rss",
        "http://rss.cnn.com/rss/edition_travel.rss",
        "http://rss.cnn.com/rss/edition_tennis.rss",
        "http://rss.cnn.com/rss/edition_motorsport.rss",
        "http://rss.cnn.com/rss/edition_golf.rss",
        "http://rss.cnn.com/rss/edition_football.rss",
        "http://rss.cnn.com/rss/edition_sport.rss",
        "http://rss.cnn.com/rss/edition_entertainment.rss",
        "http://rss.cnn.com/rss/edition_space.rss",
    ],
    Nytrss: [
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Americas.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Education.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Upshot.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Dealbook.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Baseball.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/CollegeBasketball.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/CollegeFootball.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Golf.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Hockey.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/ProBasketball.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/ProFootball.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Soccer.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Tennis.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Space.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Well.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/ArtandDesign.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Books/Review.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Dance.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Movies.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Music.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Television.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Theater.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/DiningandWine.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Weddings.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/tmagazine.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Jobs.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/RealEstate.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Automobiles.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Lens.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Obituaries.xml",
        "https://content.api.nytimes.com/svc/news/v3/all/recent.rss",
        "https://rss.nytimes.com/services/xml/rss/nyt/MostEmailed.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/MostShared.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/MostViewed.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/charles-m-blow/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/jamelle-bouie/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/david-brooks/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/frank-bruni/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/gail-collins/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/ross-douthat/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/maureen-dowd/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/thomas-l-friedman/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/michelle-goldberg/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/ezra-klein/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/nicholas-kristof/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/paul-krugman/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/farhad-manjoo/rss.xml",
        "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/bret-stephens/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/sunday-review.xml",
    ]
}

db = Database()
universities = db.session.query(Universities).all()
uni_kw = {}
uni_kw2 = {}
for uni in universities:
    uni_kw[uni] = uni.keywords_from_news.split(" | ")
    # uni_kw2[uni] = list(map(lambda z: z.strip(), uni.words_to_determine_atisimitics_event.split(',')))
words_to_save = ['jewish', 'students']

def main():
    for site_obj in links:
        o = site_obj()
        for link in links[site_obj]:
            logger.info(link)
            o.link = link
            o.parce()
            items = o.items
            logger.info(len(items))
            save_(items)

def save_(items):
    for item in items:
        if item.get('title') or item.get('text'):
            pass
        else: continue
        if all(list(map(lambda z: z in str(item['title']) or z in str(item['text']), words_to_save))):
            logger.info(f"save item")
            m, created = RelatedArticles.get_or_create(
                db.session, 
                defaults={
                    **item
                },
                title=item['title']
            )
            for uni in uni_kw: 
                if (any(list(map(lambda z: z in str(item['title']), uni_kw[uni]))) or any(list(map(lambda z: z in str(item['text']), uni_kw[uni])))): #and \
                    # (any(list(map(lambda z: z in item['title'], uni_kw2[uni]))) or any(list(map(lambda z: z in item['text'], uni_kw2[uni])))):
                    logger.info(f"add relation for {m.id} to uni {uni.id}")
                    m.university = [*m.university, uni]
                    m.state = [*m.state, uni.state]
                    db.session.commit()
        else:
            logger.debug('Skip item by word to save')
            continue


if __name__ == '__main__':
    try:
        main()
    except:
        logger.error("Exception", exc_info=True)
