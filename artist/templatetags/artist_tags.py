from datetime import timedelta, datetime
from artist.models import ArtistAccess, ArtistAssets, ArtistUserStatus
from django import template
from venue.models import VenuePictures
from customer.models import CustomerAccess

register = template.Library()


@register.filter
def has_access_to_artist(user):
    # you would need to do any localization of the result here
    return ArtistAccess.objects.filter(access=user)


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
def has_access_to_customer(user, customer):
    if CustomerAccess.objects.filter(customer=customer, access=user, admin=True):
        return 1


@register.filter
def get_image(venue):
    venue_pictures_obj = VenuePictures.objects.filter(venue=venue)
    if venue_pictures_obj:
        return venue_pictures_obj.first().file.url


@register.filter
def artist_contracts_count(artist):
    return artist.contract_set.all().count()


@register.filter
def artist_viewers_count(artist):
    try:
        return ArtistAccess.objects.filter(artist=artist).count()
    except:
        return 0


@register.filter
def artist_assets_count(artist):
    try:
        return ArtistAssets.objects.get(artist=artist).file.count()
    except:
        return 0


@register.filter
def artist_access_status_asset(artist_access):
    return ArtistUserStatus.objects.get(
        user_access=artist_access
    ).last_asset.file.last()


@register.filter
def artist_access_status_invited(artist_access):
    return ArtistUserStatus.objects.get(user_access=artist_access).invited


@register.filter
def artist_access_status_user(artist_access):
    return ArtistUserStatus.objects.get(user_access=artist_access).last_added_user.email


@register.filter
def get_date_with_time_delta(date_today, timedelta_count):
    date_today_datetime = datetime.strptime(date_today, "%Y-%m-%d").date()
    return str(date_today_datetime + timedelta(days=timedelta_count))


@register.filter
def get_day_name_with_time_delta(date_today, timedelta_count):
    date_today_datetime = datetime.strptime(date_today, "%Y-%m-%d").date()
    new_date = date_today_datetime + timedelta(days=timedelta_count)
    return new_date.strftime("%A")


@register.filter
def get_day_name(date_today):
    date_today_datetime = datetime.strptime(date_today, "%Y-%m-%d").date()
    return date_today_datetime.strftime("%A")


@register.filter
def get_name_hidden_block_contract(contract_id):
    return f"contract_id_hidden_block_{contract_id}"


@register.inclusion_tag("tags/message_extractor.html")
def message_creator(message, user, type_of_user, link, message_type_id):

    # message_type_id = artist_id or customer_id

    return {
        "message": message,
        "user": user,
        "type_of_user": type_of_user,
        "link": link,
        "message_type_id": message_type_id,
    }
