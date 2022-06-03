from os import access
from venue.models import VenueAccess
from artist.models import Artist, ArtistAccess
from customer.models import (
    Customer,
    CustomerAccess,
    CustomerContacts,
    CustomerRequestsStorage,
)
from event.models import Event
from users.models import User
from users.services import user_handle
from contract.models import Contract


def get_customer_by_id(customer_id):
    return Customer.objects.get(pk=customer_id)


def get_customer_by_name(name):
    return Customer.objects.get(name=name)


def is_allowed_to_change(customer_id, user):
    customer = get_customer_by_id(customer_id)
    customer_access_obj = CustomerAccess.objects.get(customer=customer, access=user)
    return customer_access_obj.admin


def get_users_have_access(customer_id, user):

    customer = get_customer_by_id(customer_id)
    return CustomerAccess.objects.filter(customer=customer).exclude(access=user)


def get_customer_access_by_id(id):
    return CustomerAccess.objects.get(pk=id)


def delete_customer_access(access_id):
    get_customer_access_by_id(access_id).delete()


def get_customers_for_user(user):

    return CustomerAccess.objects.filter(access=user)


def add_user_can_change(customer, user_added, admin=True):

    CustomerAccess.objects.create(customer=customer, access=user_added, admin=admin)


def hash_info(data):

    name = data["name"]
    address = data["address"]
    zip_code = data["zip_code"]
    return hash(f"{name}{address}{zip_code}")


def get_or_create_customer_by_id(customer_id):

    customer = get_customer_by_id(customer_id)
    return CustomerContacts.objects.get_or_create(customer=customer)[0]


def contacts_exists(c_c):
    """checks if main data filled"""
    return (
        c_c.first_name
        or c_c.last_name
        or c_c.phone
        or c_c.email
        or c_c.role
        or c_c.birthdate
    )


def delete_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    customer.delete()


def delete_from_changeble(customer_id, user_id):

    customer = get_customer_by_id(customer_id)
    user = user_handle.get_user_by_id(user_id)
    try:
        CustomerAccess.objects.get(customer=customer, access=user).delete()
    except Exception as ex:
        print(ex)


def get_customer_contacts_by_id(customer_contacts_id):
    return CustomerContacts.objects.get(pk=customer_contacts_id)


def delete_customer_contacts(customer_contacts_id):
    return get_customer_contacts_by_id(customer_contacts_id).delete()


def get_avaluable_users(customer):

    taken_users = [
        us.access.email for us in CustomerAccess.objects.filter(customer=customer)
    ]
    taken_users += [us.email for us in User.objects.filter(admin=True)]
    return User.objects.exclude(email__in=taken_users)


def get_users_except_admin():
    taken_users = [us.email for us in User.objects.filter(admin=True)]
    users = User.objects.exclude(email__in=taken_users)
    return [(us.email, us.get_full_name()) for us in users]


def add_permission_to_change(customer_id, user_phone, perm_type):

    customer = get_customer_by_id(customer_id)
    user = User.objects.get(phone=user_phone)
    customer_access = CustomerAccess.objects.filter(customer=customer, access=user)
    if customer_access:
        raise Exception("Can't add user that already exists")
    perm_type_py = True if perm_type == "true" else False
    if perm_type_py:
        CustomerAccess.objects.create(customer=customer, access=user, admin=True)
    else:
        CustomerAccess.objects.create(customer=customer, access=user)


def change_permission_to_change(access_id, perm_type, user):

    customer_access_obj = CustomerAccess.objects.get(pk=access_id)
    perm_type_py = True if perm_type == "true" else False

    if perm_type_py and customer_access_obj.admin != perm_type_py:
        storage = CustomerRequestsStorage.objects.filter(
            requester=customer_access_obj.access,
            owner=user,
            customer=customer_access_obj.customer,
        )
        if storage:
            storage_obj = storage.first()
            storage_obj.granted = True
            storage_obj.done = True
            storage_obj.save()
            CustomerRequestsStorage.objects.filter(
                requester=customer_access_obj.access,
                customer=customer_access_obj.customer,
            ).exclude(owner=user).delete()

    if customer_access_obj.admin != perm_type_py:
        customer_access_obj.admin = perm_type_py
        customer_access_obj.save()

    return customer_access_obj.customer


def get_customer_request_storage_by_id(request_storage_id):
    return CustomerRequestsStorage.objects.get(pk=request_storage_id)


def delete_customer_request_storage(request_storage_id):
    get_customer_request_storage_by_id(request_storage_id).delete()


def add_customer_contacts(customer_contacts, cleaned_data):

    contact_user = cleaned_data["contact_user"]
    user = user_handle.get_user_by_email(contact_user)
    signatory_rights = cleaned_data["signatory_rights"]
    active = cleaned_data["active"]
    role = cleaned_data["role"]

    customer_contacts.first_name = user.first_name
    customer_contacts.last_name = user.last_name
    customer_contacts.phone = user.phone
    customer_contacts.email = user.email
    customer_contacts.birthdate = user.birthdate
    customer_contacts.signatory_rights = signatory_rights
    customer_contacts.role = role
    customer_contacts.active = active

    customer_contacts.save()


def get_avaluable_artists(customer):

    made_contracts = [el.artist.id for el in Contract.objects.filter(customer=customer)]
    return Artist.objects.exclude(id__in=made_contracts)


def get_my_contracts(customer):

    return Contract.objects.filter(customer=customer)


def add_perm_to_see_all_types(customer_id, user_phone):
    # add permission to see all artists, venues
    # that user who invited another user to team
    user = user_handle.get_user_by_phone(user_phone)
    customer = get_customer_by_id(customer_id)
    customer_contracts = Contract.objects.filter(customer=customer)
    for elem in customer_contracts:
        perm_to_see_art = ArtistAccess.objects.filter(artist=elem.artist, access=user)
        if not perm_to_see_art:
            ArtistAccess.objects.create
        perm_to_see_venue = VenueAccess.objects.filter(venue=elem.venue, access=user)
        if not perm_to_see_venue:
            VenueAccess.objects.create(venue=elem.venue, access=user)


def delete_perm_to_see_all_types(customer_id, user_id):
    # delete permission to see all artists, venues
    # that user who invited another user to team
    user = user_handle.get_user_by_id(user_id)
    customer = get_customer_by_id(customer_id)
    customer_contracts = Contract.objects.filter(customer=customer)
    for elem in customer_contracts:
        perm_to_see_art = ArtistAccess.objects.filter(artist=elem.artist, access=user)
        if perm_to_see_art:
            perm_to_see_art.first().delete()
        perm_to_see_venue = VenueAccess.objects.filter(venue=elem.venue, access=user)
        if perm_to_see_venue:
            perm_to_see_venue.first().delete()


def add_team_peermission_to_change_contract_details(contract_obj):
    customer = contract_obj.customer
    customer_access = CustomerAccess.objects.filter(customer=customer)
    for elem in customer_access:
        perm_to_see_art = ArtistAccess.objects.filter(
            artist=contract_obj.artist, access=elem.access
        )
        if not perm_to_see_art:
            ArtistAccess.objects.create(artist=contract_obj.artist, access=elem.access)
        perm_to_see_venue = VenueAccess.objects.filter(
            venue=contract_obj.venue, access=elem.access
        )
        if not perm_to_see_venue:
            VenueAccess.objects.create(venue=contract_obj.venue, access=elem.access)


def get_customer_contact(customer):

    return CustomerContacts.objects.get(customer=customer)
