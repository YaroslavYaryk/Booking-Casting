from django import template
from event.models import EventTeam

register = template.Library()



@register.filter
def has_access_to_event(user):
    # you would need to do any localization of the result here
    return EventTeam.objects.filter(user = user)
