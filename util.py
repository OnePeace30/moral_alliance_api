import logging
import os
import sqlalchemy as sa

from io import StringIO
from sqlalchemy.orm import sessionmaker
from html.parser import HTMLParser
from contextlib import contextmanager
from configparser import ConfigParser, NoOptionError

from models import  Base


mode = 'DEFAULT'

config = ConfigParser()
current_path = os.path.dirname(__file__)
config_file = os.path.join(current_path, 'config.ini')
config.read(config_file)
try:
    DB_USER = config.get(mode, 'db_user')
    DB_PWD = config.get(mode, 'db_pwd')
    DB_HOST = config.get(mode, 'db_host')
    DB_PORT = config.get(mode, 'db_port')
    DB_NAME = config.get(mode, 'db_name')
except NoOptionError:
    raise

logger = logging.getLogger('moral_allince')

main_engine = sa.create_engine(
    f'postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    echo=True,
)


class Database():

    def __init__(self):
        logger.info('Init database connection')
        DBSession = sessionmaker(
            binds={
                Base: main_engine,
            },
            expire_on_commit=False,
        )
        self.session = DBSession()

    def __del__(self):
        logger.info('Close database connection')
        self.session.close()

    @contextmanager
    def session_scope(self):
        try:
            yield self.session
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    # django like method
    def get_or_create(self, model, defaults=None, **kwargs):
        with self.session_scope() as session:
            instance = session.query(model).filter_by(**kwargs).one_or_none()
            if instance:
                return instance, False
            else:
                kwargs |= defaults or {}
                instance = model(**kwargs)
                try:
                    session.add(instance)
                    session.commit()
                except Exception:
                    session.rollback()
                    instance = session.query(model).filter_by(**kwargs).one()
                    return instance, False
                else:
                    return instance, True


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()