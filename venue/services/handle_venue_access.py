from venue.models import VenueAccess


def get_venue_access_by_id(access_id):
    return VenueAccess.objects.get(pk=access_id)

def delete_venue_access(access_id):
    get_venue_access_by_id(access_id).delete()
