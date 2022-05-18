from multiprocessing import context

from artist.models import ArtistAccess
from django import template
from venue.models import VenuePictures

register = template.Library()


@register.filter
def has_access_to_artist(user):
    # you would need to do any localization of the result here
    return ArtistAccess.objects.filter(access = user)

@register.filter
def get_ev_artist_id(object):
    # you would need to do any localization of the result here
    return f"object_artist_{object.id}"

@register.filter
def get_ev_artist_form_id(object):
    # you would need to do any localization of the result here
    return f"form_object_artist_{object.id}"


@register.filter
def get_info(object):
    # you would need to do any localization of the result here
    return type(object)

@register.filter
def get_image(venue):
    venue_pictures_obj =  VenuePictures.objects.filter(venue = venue)
    if venue_pictures_obj:
        return venue_pictures_obj.first().file.url



@register.inclusion_tag("tags/message_extractor.html")
def message_creator(message, user,type_of_user, link, message_type_id):

    # message_type_id = artist_id or customer_id

	return {
        "message" : message,
        "user": user,
        "type_of_user": type_of_user,
        "link": link,
        "message_type_id" : message_type_id
    }
