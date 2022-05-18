from venue.models import VenueAccess, VenueRequestsStorage

from .handle_venue import get_venue_by_id


def send_request(user, venue_id):
    venue = get_venue_by_id(venue_id)
    
    user_access_obj = VenueAccess.objects.filter(venue=venue, admin=True)
    if user_access_obj:
        for access_user in user_access_obj:
            VenueRequestsStorage.objects.create(requester = user, 
                                                 owner = access_user.access, 
                                                 venue = venue)

def get_venue_request_storage_by_id(request_storage_id):
    return VenueRequestsStorage.objects.get(pk=request_storage_id)


def delete_venue_request_storage(request_storage_id):
    get_venue_request_storage_by_id(request_storage_id).delete()
