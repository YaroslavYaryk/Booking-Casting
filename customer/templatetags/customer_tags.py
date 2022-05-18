from customer.models import CustomerAccess
from django import template

register = template.Library()



@register.filter
def has_access_to_customer(user):
    # you would need to do any localization of the result here
    return CustomerAccess.objects.filter(access = user)
