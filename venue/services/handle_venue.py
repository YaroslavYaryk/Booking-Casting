from http.client import ImproperConnectionState

from django.db.models import Q
from event.models import Event
from users.models import User
from users.services import user_handle
from venue.models import (Venue, VenueAccess, VenueContacts, VenuePictures,
                          VenueRequestsStorage)


def get_customers_for_user(user):
    return VenueAccess.objects.filter(access=user)

def get_venue_by_id(id):
    return Venue.objects.get(pk=id)


def add_user_can_change(venue_obj,user, admin=True):
    
    VenueAccess.objects.create(venue=venue_obj, access=user, admin=admin)


def is_allowed_to_change(venue_id, user):
    venue = get_venue_by_id(venue_id)
    venue_access = VenueAccess.objects.get(venue=venue, access=user)
    return venue_access.admin
    
    
def get_users_can_change(venue_id, user):
    venue = get_venue_by_id(venue_id)
    return VenueAccess.objects.filter(venue=venue).exclude(access=user)

def get_avaluable_users(venue):
    taken_users = [us.access.email for us in VenueAccess.objects.filter(venue=venue)]
    taken_users += [us.email for us in User.objects.filter(admin=True)]
    return User.objects.exclude(email__in = taken_users)


def add_permission_to_change(venue_id, user_email, perm_type):
    venue = get_venue_by_id(venue_id)
    user = User.objects.get(email=user_email)
    venue_access = VenueAccess.objects.filter(venue=venue, access=user)
    if venue_access:
        raise Exception("Can't add user that already exists")
    perm_type_py = True if perm_type == 'true' else False
    if perm_type_py:
        VenueAccess.objects.create(venue = venue, access=user, admin=True)
    else:
        VenueAccess.objects.create(venue = venue, access=user)


def change_permission_to_change(access_id, perm_type, user):
    
    venue_access_obj = VenueAccess.objects.get(pk=access_id)
    perm_type_py = True if perm_type == 'true' else False
    
    # when user asks permission admin can approve it or deny
    # if request sent we check if admin aprove
    # when it was false and became true
    if perm_type_py and venue_access_obj.admin != perm_type_py:
        storage = VenueRequestsStorage.objects.filter(requester=venue_access_obj.access, owner=user, venue=venue_access_obj.venue)
        if storage:
            storage_obj = storage.first()
            storage_obj.granted = True
            storage_obj.done = True
            storage_obj.save()
            VenueRequestsStorage.objects.filter(requester=venue_access_obj.access, venue=venue_access_obj.venue).exclude(owner=user).delete()
    
    if venue_access_obj.admin != perm_type_py:
        venue_access_obj.admin = perm_type_py
        venue_access_obj.save()
        
    
    return venue_access_obj.venue


def get_all_messages_for_user(user):
    messages = VenueRequestsStorage.objects.filter(Q(requester=user) | Q(owner=user)).order_by("-created_at")
    return messages


def delete_venue(venue_id):
    venue = get_venue_by_id(venue_id)
    venue.delete()


def delete_from_changeble(venue_id, user_id):
    venue = get_venue_by_id(venue_id)
    user = user_handle.get_user_by_id(user_id)
    VenueAccess.objects.get(venue=venue, access=user).delete()


def get_venue_pictures(venue_id):
    venue = get_venue_by_id(venue_id)
    return VenuePictures.objects.filter(venue=venue)


def delete_venue_picture(picture_id):
    VenuePictures.objects.get(pk=picture_id).delete() 


def get_venue_contacts_by_id(venue_contacts_id):
    return VenueContacts.objects.get(pk=venue_contacts_id)


def delete_venue_contacts(venue_contacts_id):
    get_venue_contacts_by_id(venue_contacts_id).delete()


def get_my_events(venue_id):
    return Event.objects.filter(venue__id=venue_id)
