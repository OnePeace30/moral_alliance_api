import typing as T
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import _sa_util
import sqlalchemy as sa



class Base(DeclarativeBase):

    __abstract__ = True

    @classmethod
    def get_or_create(
        cls, session: sa.orm.Session, defaults=None, commit=True, **kwargs
    ):
        """Django-inspired get_or_create."""
        predicates = [getattr(cls, k) == v for k, v in kwargs.items()]
        instance = session.scalar(sa.select(cls).where(*predicates))
        if instance:
            return instance, False

        defaults = defaults or {}
        instance_kwargs = kwargs | defaults
        instance = cls(**instance_kwargs)
        session.add(instance)
        if commit:
            session.commit()

        return instance, True

article_to_uni = sa.Table('article_to_uni', Base.metadata, 
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('uni_id', sa.Integer(), ForeignKey("universities.id")),
    sa.Column('article_id', sa.Integer(), ForeignKey("related_articles.id"))
)

article_to_state = sa.Table('article_to_state', Base.metadata, 
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('state_id', sa.Integer(), ForeignKey("states.id")),
    sa.Column('artical_id', sa.Integer(), ForeignKey("related_articles.id"))
)

class State(Base):
    __tablename__ = 'states'

    id = sa.Column(sa.Integer, primary_key=True)
    state_safe_index = sa.Column(sa.Integer, nullable=True)
    population = sa.Column(sa.Integer, nullable=True)
    uni_count = sa.Column(sa.Integer, nullable=True)
    name = sa.Column(sa.String(255), nullable=True)
    state_governor = sa.Column(sa.String(255), nullable=True)
    region = sa.Column(sa.String(255), nullable=True)
    offical_statment = sa.Column(sa.String(255), nullable=True)
    center_lng = sa.Column(sa.Numeric, nullable=True)
    center_lat = sa.Column(sa.Numeric, nullable=True)
    hate_speech_growth = sa.Column(sa.Numeric, nullable=True)
    hate_in_fraction_growth = sa.Column(sa.Numeric, nullable=True)
    relative_state_size = sa.Column(sa.Numeric, nullable=True)
    logo = sa.Column(sa.Text, nullable=True)

    @property
    def point(self):
        return "states"

class Universities(Base):
    __tablename__ = 'universities'

    id = sa.Column(sa.Integer, primary_key=True)
    num_of_students = sa.Column(sa.Integer, nullable=True)
    safe_score = sa.Column(sa.Integer, nullable=True)
    name = sa.Column(sa.String(255), nullable=True)
    president_name = sa.Column(sa.String(255), nullable=True)
    status = sa.Column(sa.String(45), nullable=True)
    status_direction = sa.Column(sa.String(45), nullable=True)
    map_statement = sa.Column(sa.String(255), nullable=True)
    address = sa.Column(sa.String(255), nullable=True)
    hate_speech_in_fraction_desc = sa.Column(sa.String(255), nullable=True)
    hate_speech_growth_desc = sa.Column(sa.String(255), nullable=True)
    state_id = sa.Column(sa.Integer, sa.ForeignKey('states.id'))
    lng = sa.Column(sa.Numeric, nullable=True)
    lat = sa.Column(sa.Numeric, nullable=True)
    hate_speech_score = sa.Column(sa.Numeric, nullable=True)
    hate_infraction_score = sa.Column(sa.Numeric, nullable=True)
    social_media_harassment = sa.Column(sa.Numeric, nullable=True)
    harrasment_on_campus = sa.Column(sa.Numeric, nullable=True)
    hate_speech_in_fraction = sa.Column(sa.Numeric, nullable=True)
    hate_speech_growth = sa.Column(sa.Numeric, nullable=True)
    logo = sa.Column(sa.Text, nullable=True)
    offical_statment = sa.Column(sa.Text, nullable=True)
    about = sa.Column(sa.Text, nullable=True)
    contact_university = sa.Column(sa.Text, nullable=True)
    keywords_from_news = sa.Column(sa.String, nullable=True)
    words_to_determine_atisimitics_event = sa.Column(sa.String, nullable=True)
    status_desc = sa.Column(sa.String(45), nullable=True)
    status_sub = sa.Column(sa.String(45), nullable=True)

    posts = sa.orm.relationship("SMPosts", back_populates="university")
    events = sa.orm.relationship("Events", back_populates="university")

class Sources(Base):
    __tablename__ = "sources"

    link_to_state = sa.Column(sa.Text, name='Link to state news 1', nullable=True)
    domain = sa.Column(sa.Text, name='domain', nullable=True, primary_key=True)
    link = sa.Column(sa.Text, name='link to google news', nullable=True)
    score = sa.Column(sa.Text, name='score of relevance to the university', nullable=True)
    words = sa.Column(sa.Text, name='Words to determine atisimitics event', nullable=True)
    university_name = sa.Column(sa.Text, name='University name1', nullable=True)
    state_name = sa.Column(sa.Text, name='State name1', nullable=True)
    university_id = sa.Column(sa.Text, sa.ForeignKey('universities.id'), name='university_id', nullable=True)
    state_id = sa.Column(sa.Text, sa.ForeignKey('states.id'), name='state_id', nullable=True)
    university = relationship('Universities')
    state = relationship('State')

class RelatedArticles(Base):
    __tablename__ = 'related_articles'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255), nullable=True)
    link = sa.Column(sa.Text, nullable=True)
    text = sa.Column(sa.Text, nullable=True)
    pic = sa.Column(sa.Text, nullable=True)
    date = sa.Column(sa.DATETIME, nullable=True)
    to_send = sa.Column(sa.Boolean, default=False)
    rank = sa.Column(sa.Integer, nullable=True)
    
    university = sa.orm.relationship("Universities", secondary=article_to_uni, backref="articles")
    state = sa.orm.relationship("State", secondary=article_to_state, backref="articles")


class AlumniAll(Base):
    __tablename__ = 'alumni_all'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(255), nullable=True)
    last_name = sa.Column(sa.String(255), nullable=True)
    link_to_main = sa.Column(sa.String(255), nullable=True)
    link_to_linkdin = sa.Column(sa.String(255), nullable=True)
    link_to_tw = sa.Column(sa.String(255), nullable=True)
    link_to_fc = sa.Column(sa.String(255), nullable=True)
    link_to_inst = sa.Column(sa.String(255), nullable=True)
    title = sa.Column(sa.String(255), nullable=True)
    university = sa.Column(sa.String(255), nullable=True)
    person_id = sa.Column(sa.String(255), nullable=True)
    email = sa.Column(sa.String(255), nullable=True)
    email_status = sa.Column(sa.String(255), nullable=True)
    github_url = sa.Column(sa.String(255), nullable=True)
    headline = sa.Column(sa.String(255), nullable=True)
    present_raw_address = sa.Column(sa.String(255), nullable=True)
    industry = sa.Column(sa.String(255), nullable=True)
    employees = sa.Column(sa.String(255), nullable=True)
    organization = sa.Column(sa.String(255), nullable=True)
    phone_numbers = sa.Column(sa.String(255), nullable=True)
    phone = sa.Column(sa.String(255), nullable=True)
    uni_id = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), name='uni_id', nullable=True)


class AlumniNotable(Base):
    __tablename__ = 'alumni_notable'
    
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(255), nullable=True)
    last_name = sa.Column(sa.String(255), nullable=True)
    title = sa.Column(sa.String(255), nullable=True)
    photo = sa.Column(sa.Text, nullable=True)
    uni_id = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), name='uni_id', nullable=True)

    university = sa.orm.relationship("Universities")


class HateGroups(Base):
    __tablename__ = "hate_groups"

    id = sa.Column(sa.Integer, primary_key=True)
    group_name = sa.Column(sa.String(255), nullable=True)
    group_link = sa.Column(sa.String(255), nullable=True)
    status = sa.Column(sa.String(45), nullable=True)
    uni_name = sa.Column(sa.String(255), nullable=True)
    uni = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), name='uni_id', nullable=True)


class Gifts(Base):
    __tablename__ = 'gifts'

    id = sa.Column(sa.Integer, primary_key=True)
    country = sa.Column(sa.String, nullable=True)
    sumofdonations = sa.Column(sa.Integer, nullable=True)
    year = sa.Column(sa.Integer, nullable=True)
    percentage = sa.Column(sa.Numeric, nullable=True)
    university_id = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), name='university_id', nullable=True)


class SMPosts(Base):
    __tablename__ = 'sm_posts'

    id = sa.Column(sa.Integer, primary_key=True)
    sentiment = sa.Column(sa.Integer, nullable=True)
    id_word = sa.Column(sa.Integer, nullable=True)
    number_comments = sa.Column(sa.Integer, nullable=True)
    number_likes = sa.Column(sa.Integer, nullable=True)
    score = sa.Column(sa.Integer, nullable=True)
    network = sa.Column(sa.String(255), nullable=True)
    author_name = sa.Column(sa.String(255), nullable=True)
    link = sa.Column(sa.String(255), nullable=True)
    community = sa.Column(sa.String(255), nullable=True)
    domain = sa.Column(sa.String(255), nullable=True)
    post_text = sa.Column(sa.Text, nullable=True)
    image = sa.Column(sa.Text, nullable=True)
    uni_id = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), name='uni_id', nullable=True)
    date_added_to_db = sa.Column(sa.DATETIME, nullable=True)
    post_create = sa.Column(sa.DATETIME, nullable=True)

    university = sa.orm.relationship("Universities", back_populates="posts")


class Events(Base):
    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=True)
    event_type = sa.Column(sa.Text, nullable=True)
    event_tags = sa.Column(sa.Text, nullable=True)
    street_address = sa.Column(sa.Text, nullable=True)
    state = sa.Column(sa.Text, nullable=True)
    organizing_group = sa.Column(sa.Text, nullable=True)
    organizing_chapters = sa.Column(sa.Text, nullable=True)
    researcher_comment = sa.Column(sa.Text, nullable=True)
    date = sa.Column(sa.DateTime, nullable=True)
    lng = sa.Column(sa.DECIMAL, nullable=True)
    lat = sa.Column(sa.DECIMAL, nullable=True)
    uni_id = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), name='uni_id', nullable=True)

    university = sa.orm.relationship("Universities", back_populates="events")


class EventsAnnotated(Base):
    __tablename__ = 'events_annotated'

    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.String(), nullable=False)
    month_label = sa.Column(sa.String(), nullable=False)
    amount = sa.Column(sa.Integer, nullable=False)
    university_id = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), nullable=True)


class UniversityPost(Base):
    __tablename__ = 'university_posts'

    id = sa.Column(sa.Integer, primary_key=True)
    uni_id = sa.Column(sa.Integer, sa.ForeignKey('universities.id'), name='uni_id', nullable=True)
    uni_name = sa.Column(sa.Text, nullable=True)
    text = sa.Column(sa.Text, nullable=True)
    author = sa.Column(sa.Text, nullable=True)
    social_media = sa.Column(sa.Text, nullable=True, name='social media')
    direct_link = sa.Column(sa.Text, nullable=True, name='direct link')
    month_year = sa.Column(sa.DateTime, nullable=True, name='month year')
