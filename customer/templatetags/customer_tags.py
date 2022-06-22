from customer.models import CustomerAccess
from django import template
from contract.models import ContractEventTeam

register = template.Library()


@register.filter
def has_access_to_customer(user):
    # you would need to do any localization of the result here
    return CustomerAccess.objects.filter(access=user)


@register.filter
def user_hass_access_to_contract(user):
    if user.is_authenticated:
        return ContractEventTeam.objects.filter(user=user)
