from venue.models import VenueContacts

from .handle_venue import get_venue_by_id


def get_or_create_customer_by_id(venue_id):
    venue = get_venue_by_id(venue_id)
    return VenueContacts.objects.get_or_create(venue=venue)[0]


def contacts_exists(c_c):
    """ checks if main data filled """
    return c_c.first_name or c_c.last_name or c_c.phone or c_c.epost or c_c.role 
