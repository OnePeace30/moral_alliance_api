from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

from models import Events
from util import Database



geolocator = Nominatim(user_agent="pythonsheets")
def main():
    db = Database()
    events = db.session.query(Events).filter(Events.lng == None)
    for event in events:
        
        lng, lat = address_geocode(event)
        print(event , lng, lat, sep=' - ')
        event.lng = lng
        event.lat = lat
        db.session.commit()


def address_geocode(e):
    try:
        address = f"{e.street_address}"
        print(address)
        location = geolocator.geocode(address, timeout=100)
        return location.longitude, location.latitude
    except (AttributeError, GeocoderServiceError) as err:
        print(err)
        return None, None

if __name__ in ['django.core.management.commands.shell', '__main__']:
    main()
