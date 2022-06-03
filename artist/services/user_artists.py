from django.core import mail
from artist.models import (
    Artist,
    ArtistAccess,
    ArtistAssets,
    ArtistFile,
    ArtistRequestsStorage,
    ArtistUserStatus,
)
from users.models import User
from users.services import user_handle
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_artists_for_user(user):
    return ArtistAccess.objects.filter(access=user)


def get_artist_by_name(name):
    return Artist.objects.get(name=name)


def get_artist_by_id(artist_id):
    return Artist.objects.get(pk=artist_id)


def add_artist_access(artist, user):

    ArtistAccess.objects.create(artist=artist, access=user, admin=True)


def get_artist_access_by_id(id):
    return ArtistAccess.objects.get(pk=id)


def delete_artist_access(id):
    ArtistAccess.objects.get(pk=id).delete()


def is_allowed_to_change(artist_id, user):
    artist = get_artist_by_id(artist_id)
    artist_access_obj = ArtistAccess.objects.get(artist=artist, access=user)
    return artist_access_obj.admin


def delete_artist(artist_id):
    artist = get_artist_by_id(artist_id)
    artist.delete()


def get_artist_owner(artist_id):
    artist = get_artist_by_id(artist_id)
    return artist.owner_creator


def get_artist_assets(artist_id):

    artist = get_artist_by_id(artist_id)
    return ArtistAssets.objects.get_or_create(artist=artist)[0]


def get_assets_by_id(id):
    return ArtistAssets.objects.get(pk=id)


def delete_artist_assets(assets_id):
    get_assets_by_id(assets_id).delete()


def save_artist_assets(artist_assets, credit_name, files):

    images = files.getlist("pdf")
    for image in images:
        artist_file = ArtistFile.objects.create(name=image.name, file=image)
        artist_assets.file.add(artist_file)

    if credit_name:
        artist_assets.credit = credit_name

    artist_assets.save()


def get_file_by_id(id):
    return ArtistFile.objects.get(pk=id)


def delete_artist_file(file_id):

    return get_file_by_id(file_id).delete()


def get_users_have_access(artist_id, user):

    artist = get_artist_by_id(artist_id)
    return ArtistAccess.objects.filter(artist=artist).exclude(access=user)


def delete_from_changeble(artist_id, user_id):

    artist = get_artist_by_id(artist_id)
    user = user_handle.get_user_by_id(user_id)

    try:
        ArtistAccess.objects.get(artist=artist, access=user).delete()
    except Exception as ex:
        print(ex)


def get_file_by_id(file_id):
    return ArtistFile.objects.get(pk=file_id)


def delete_artist_file(file_id):

    get_file_by_id(file_id).delete()


def get_artist_request_storage_by_id(request_storage_id):
    return ArtistRequestsStorage.objects.get(pk=request_storage_id)


def delete_artist_request_storage(request_storage_id):
    get_artist_request_storage_by_id(request_storage_id).delete()


def get_avaluable_users(artist):

    taken_users = [us.access.email for us in ArtistAccess.objects.filter(artist=artist)]
    taken_users += [us.email for us in User.objects.filter(admin=True)]
    return User.objects.exclude(email__in=taken_users)


def add_permission_to_change(artist_id, user_phone, perm_type):
    artist = get_artist_by_id(artist_id)
    user = User.objects.get(phone=user_phone)
    artist_access = ArtistAccess.objects.filter(artist=artist, access=user)
    if artist_access:
        raise Exception("Can't add user that already exists")
    perm_type_py = True if perm_type == "true" else False
    if perm_type_py:
        ArtistAccess.objects.create(artist=artist, access=user, admin=True)
    else:
        ArtistAccess.objects.create(artist=artist, access=user)


def change_permission_to_change(access_id, perm_type, user):
    artist_obj = ArtistAccess.objects.get(pk=access_id)
    perm_type_py = True if perm_type == "true" else False

    if perm_type_py and artist_obj.admin != perm_type_py:
        storage = ArtistRequestsStorage.objects.filter(
            requester=artist_obj.access, owner=user, artist=artist_obj.artist
        )
        if storage:
            storage_obj = storage.first()
            storage_obj.granted = True
            storage_obj.done = True
            storage_obj.save()
            ArtistRequestsStorage.objects.filter(
                requester=artist_obj.access, artist=artist_obj.artist
            ).exclude(owner=user).delete()

    if artist_obj.admin != perm_type_py:
        artist_obj.admin = perm_type_py
        artist_obj.save()

    return artist_obj.artist


def send_invitation_message(sender, reciever, template_link, site_link):
    subject = "Invitation Message"
    html_message = render_to_string(
        template_link, {"sender": sender, "site_link": site_link}
    )
    plain_message = strip_tags(html_message)
    from_email = "bookingdjangoprojkpi@gmail.com"
    to = reciever

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def get_artist_contracts(artist, date):
    return artist.contract_set.filter(date=date)


def get_all_artist_contracts(artist):
    return artist.contract_set.all()


def create_user_access_status(artist_id, user_phone):
    artist = get_artist_by_id(artist_id)
    user = user_handle.get_user_by_phone(user_phone)
    user_access = ArtistAccess.objects.get(artist=artist, access=user)
    ArtistUserStatus.objects.create(user_access=user_access, invited=True)
