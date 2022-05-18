
from artist.models import Artist, ArtistAccess, ArtistRequestsStorage
from django.db.models import Q
from users.services import user_handle

from .user_artists import get_artist_by_id


def send_request(user, artist_id):
    artist = get_artist_by_id(artist_id)
    user_access_obj = ArtistAccess.objects.filter(artist=artist, admin=True)
    if user_access_obj:
        for access_user in user_access_obj:
            ArtistRequestsStorage.objects.create(requester = user, 
                                                 owner = access_user.access, 
                                                 artist = artist)
    

def get_artist_messages_for_user(user):
    
    messages = ArtistRequestsStorage.objects.filter(Q(requester=user) | Q(owner=user)).order_by("-created_at")
    return messages


def handle_request_form(r_from, r_to, artist_id, choice, granted):
    print("worked")
    requester = user_handle.get_user_by_id(r_from)
    owner = user_handle.get_user_by_id(r_to)
    artist = get_artist_by_id(artist_id)
    
    deal = ArtistRequestsStorage.objects.get(requester = requester, owner = owner, artist = artist)
    artist_access_obj = ArtistAccess.objects.filter(artist = artist)
    if granted:
        artist.user.add(requester)
        deal.granted = True
        
        if choice:
            if artist_access_obj:
                artist_access_obj.first().access.add(requester)
            else:
                ArtistAccess.objects.create(artist = artist, admin=True)
    
    deal.done = True        
    deal.save()
