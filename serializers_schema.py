from models import (State, Universities, RelatedArticles,
                    HateGroups, Gifts, SMPosts, AlumniNotable,
                    EventsAnnotated)

class Field:
    pass

class ModelFieldSerializer(Field):
    
    def __init__(self, field_name):
        self.field_name = field_name

    def to_representation(self, obj, field=None):
        if self.field_name is None:
            _field = field
        else:
            _field = self.field_name
        return getattr(obj, _field)


class FloatFieldSerializer(ModelFieldSerializer):

    def __init__(self, field_name=None):
        self.field_name = field_name

    def to_representation(self, obj, field):
        data = super().to_representation(obj, field)
        if data is None: return None
        return float(data)

class SerializerMethodField(object):

    def __init__(self, method_name=None):
        self.method_name = method_name

    def to_representation(self, serializer, field):
        if self.method_name is None:
            method = f'get_{field}'
        else:
            method = self.method_name
        return getattr(serializer, method)(serializer.instance)

class BaseSerializer(object):

    def __init__(self, istance):
        self._data = {}
        self.instance = istance

    @property
    def data(self):
        self.serialize()
        return self._data

    class Meta:
        model = None
        fields = []

    def serialize(self):
        if self.Meta.model is None:
            raise AssertionError("The model not set")
        for field in self.Meta.fields:
            if hasattr(self, field):
                if isinstance(getattr(self, field), Field):
                    self._data[field] = getattr(self, field).to_representation(self.instance, field)
                elif isinstance(getattr(self, field), SerializerMethodField):
                    self._data[field] = getattr(self, field).to_representation(self, field)
            elif hasattr(self.Meta.model, field):
                self._data[field] = getattr(self.instance, field)
            else:
                raise Exception('qwerty')


class StateSerializer(BaseSerializer):
    centerLng = FloatFieldSerializer('center_lng')
    centerLat = FloatFieldSerializer('center_lat')
    size = FloatFieldSerializer('relative_state_size')
    hateSpeechGrowth = FloatFieldSerializer('hate_speech_growth')
    hateInfractionGrowth = FloatFieldSerializer('hate_in_fraction_growth')
    stateSafeIndex = ModelFieldSerializer('state_safe_index')
    stateGoverner = ModelFieldSerializer('state_governor')
    uniCount = ModelFieldSerializer('uni_count')
    officialStatement = ModelFieldSerializer('offical_statment')

    class Meta:
        model = State
        fields = (
            "id","name","logo","centerLng",
            "centerLat","size","hateSpeechGrowth",
            "hateInfractionGrowth","stateSafeIndex",
            "stateGoverner","population","uniCount",
            "officialStatement","region",
        )

class UniversitiesSerializer(BaseSerializer):
    state = ModelFieldSerializer('state_id')
    lng = FloatFieldSerializer()
    lat = FloatFieldSerializer()
    hateSpeechGrowth = FloatFieldSerializer('hate_speech_growth')
    hateInfractionGrowth = FloatFieldSerializer('hate_speech_in_fraction')
    hateSpeechScore = FloatFieldSerializer('hate_speech_score')
    hateInfractionScore = FloatFieldSerializer('hate_infraction_score')
    socialMediaHarassemnt = FloatFieldSerializer('social_media_harassment')
    harassmentOnCampus = FloatFieldSerializer('harrasment_on_campus')
    president = ModelFieldSerializer('president_name')
    studentCount = ModelFieldSerializer('num_of_students')
    officialStatement = ModelFieldSerializer('offical_statment')
    safeScore = ModelFieldSerializer('safe_score')
    statusDirection = ModelFieldSerializer('status_direction')
    quote = ModelFieldSerializer('map_statement')
    contact = ModelFieldSerializer('contact_university')

    class Meta:
        model = Universities
        fields = ( 
            "id", "name", "state", "logo", 
            "lng", "lat", "hateSpeechGrowth", 
            "hateInfractionGrowth", #"quote", 
            "hateSpeechScore", "hateInfractionScore", 
            "socialMediaHarassemnt", "harassmentOnCampus", 
            "president", "studentCount", "status", 
            "statusDirection", "officialStatement", "about", 
            "address", "safeScore", "quote", 'contact'
        )

class RelatedArticlesSerializer(BaseSerializer):
    university = SerializerMethodField()
    state = SerializerMethodField()

    class Meta:
        model = RelatedArticles
        fields = ( 
            "id", "title", "pic", 
            "text", "link", "university", 
            "state",
        )

    def get_state(self, obj):
        try:
            return obj.state[0].id 
        except IndexError:
            return None
    
    def get_university(self, obj):
        try:
            return obj.university[0].id 
        except IndexError:
            return None


class HateGroupsSerializer(BaseSerializer):
    university = SerializerMethodField()
    name = ModelFieldSerializer('group_name')
    link = ModelFieldSerializer('group_link')

    class Meta:
        model = HateGroups
        fields = ( 
            "id", "name", "link", "status", 
            "university",
        )

    def get_university(self, obj):
        return obj.uni

class GiftsSerializer(BaseSerializer):
    sumOfDonations = ModelFieldSerializer('sumofdonations')
    university = ModelFieldSerializer('university_id')
    percentage = FloatFieldSerializer()

    class Meta:
        model = Gifts
        fields = ( 
            "id", "country", "sumOfDonations", 
            "year", "percentage", "university",
        )


class SMPostsSerializer(BaseSerializer):
    content = ModelFieldSerializer('post_text')
    author = ModelFieldSerializer('author_name')
    month = SerializerMethodField()
    monthLabel = SerializerMethodField()
    year = SerializerMethodField()
    university = ModelFieldSerializer('uni_id')

    class Meta:
        model = SMPosts
        fields = ( 
            "id", "network", "link", "content", 
            "author", "month", "monthLabel", 
            "year", "university",
        )

    def get_month(self, obj):
        return obj.post_create.month

    def get_monthLabel(self, obj):
        return obj.post_create.strftime("%B")
    
    def get_year(self, obj):
        return obj.post_create.year


class AlumniNotableSeralizer(BaseSerializer):
    name = SerializerMethodField()
    logo = ModelFieldSerializer('photo')
    university = ModelFieldSerializer('uni_id')

    class Meta:
        model = AlumniNotable
        fields = (
            "id",
            "name",
            "logo",
            "university",
        )

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    

class EventsAnnotatedSerializer(BaseSerializer):
    university = ModelFieldSerializer('university_id')

    class Meta:
        model = EventsAnnotated
        fields = (
            'id', 'date', 'month_label',
            'amount', 'university'
        )