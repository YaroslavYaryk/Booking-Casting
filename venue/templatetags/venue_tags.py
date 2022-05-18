from django import template
from venue.models import VenueAccess

register = template.Library()

@register.filter
def has_access_to_venue(user):
    # you would need to do any localization of the result here
    return VenueAccess.objects.filter(access = user)
