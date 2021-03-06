from django.shortcuts import render
from django.http import HttpResponse
from artist.models import Artist, ArtistAccess
from artist.services import user_artists
from company.models import Company, CompanyAccess
from customer.models import Customer, CustomerAccess
from event.models import Event, EventRentalProducts, EventTeam, RentalProducts
from jinja2 import Template
from users.models import User
from users.services import user_handle
from venue.models import Venue, VenueAccess
from event.services import constants
from contract.models import (
    CRentalProduct,
    Contract,
    CompanyContractRentalProduct,
    ContractEventTeam,
    ContractRentalProducts,
    ContractTimeClock,
    TimeClock,
    ArtistTeamEvent,
    CompanyRentalProduct,
    CompanyContractOneProduct,
)
from contract.services import handle_contract
from datetime import date, datetime, timedelta


def get_event_contracts_for_user(user, date):
    return ContractEventTeam.objects.filter(user=user, contract__date=date)


def get_upcoming_events(user, date):
    date_today_datetime = datetime.strptime(date, "%Y-%m-%d").date()
    date_from = str(date_today_datetime + timedelta(days=1))
    date_to = str(date_today_datetime + timedelta(days=20))
    return ContractEventTeam.objects.filter(
        user=user,
        contract__date__gte=date_from,
        contract__date__lte=date_to,
        contract__visible=True,
    )


def get_event_by_id(id):
    return Event.objects.get(pk=id)


def delete_event(event_id):
    get_event_by_id(event_id).delete()


def get_company_queryset(user):
    my_companies_ids = [
        el.company.id for el in CompanyAccess.objects.filter(access=user, admin=True)
    ]
    return Company.objects.filter(id__in=my_companies_ids, active=True)


def get_venue_queryset(user):

    my_venues = [el.venue.email for el in VenueAccess.objects.filter(access=user)]
    return Venue.objects.filter(email__in=my_venues, active=True)


def get_customer_queryset(user):
    my_customers = [el.customer.id for el in CustomerAccess.objects.filter(access=user)]
    return Customer.objects.filter(pk__in=my_customers, active=True)


def get_artist_queryset(user):
    my_artists = [el.artist.id for el in ArtistAccess.objects.filter(access=user)]
    return Artist.objects.filter(pk__in=my_artists, active=True)


def get_linked_text(link, id, object):
    return f""" <a style="color:black" href="../../../{link}/{id}/details/">{object}</a> """


artists = """
<ul>
    {% for obj in artists %}
        <li> <a style="color:black" href="../../../artist/{{obj.artist.id}}/artist_details/">{{obj.artist.name}}</a></li>
    {% endfor %}
</ul>
"""

# def get_final_contract(event_obj):
#     contract = Template(event_obj.contract_template)
#     customer_name = get_linked_text("customer", event_obj.customer.id, event_obj.customer.name)
#     company_name = get_linked_text("company", event_obj.company.id, event_obj.company.name)
#     venue_name = get_linked_text("venue", event_obj.venue.id, event_obj.venue.name)
#     event_artist_object = EventArtists.objects.filter(event=event_obj)
#     artists_objs = Template(artists)
#     artists_display_list = artists_objs.render(artists=event_artist_object)
#     return contract.render(customer=customer_name,company=company_name, venue=venue_name, artists=artists_display_list )


def add_user_to_event_team(event_id, user, role):
    event = get_event_by_id(event_id)
    EventTeam.objects.create(event=event, user=user, role=role)


def is_allowed_to_change(event_id, user):
    contract = handle_contract.get_contract_artist_by_id(event_id)
    return ContractEventTeam.objects.get(contract=contract, user=user)


def get_users_team(event_id, user):
    event = handle_contract.get_contract_artist_by_id(event_id)
    return ContractEventTeam.objects.filter(contract=event).exclude(user=user)


def get_avaluable_users(contract):
    taken_users = [
        us.user.email for us in ContractEventTeam.objects.filter(contract=contract)
    ]
    taken_users += [us.email for us in User.objects.filter(admin=True)]
    return User.objects.exclude(email__in=taken_users)


def get_my_artists(user):

    artist_access_obj = [
        el.artist.id
        for el in ArtistAccess.objects.filter(access=user)
        if el.artist.active
    ]
    return Artist.objects.filter(id__in=artist_access_obj)


# def get_active_artists(event_id):
#     event = get_event_by_id(event_id)
#     existing_artist_in_event = [obj.artist.id for obj in  EventArtists.objects.filter(event=event)]
#     return Artist.objects.filter(active=True).exclude(id__in = existing_artist_in_event)


# def get_event_artists(event_id):
#     event = get_event_by_id(event_id)
#     return EventArtists.objects.filter(event=event)


# def delete_artist_from_event(event_id, artist_id):
#     EventArtists.objects.get(event__id = event_id, artist__id = artist_id).delete()


# def get_event_artist_by_id(ev_artist_id):
#     return EventArtists.objects.get(pk=ev_artist_id)


def is_allowed_to_change(event_id, user):
    return ContractEventTeam.objects.get(contract__id=event_id, user=user)


def add_user_to_team(contract_id, us_email, role):
    contract = handle_contract.get_contract_artist_by_id(contract_id)
    user = user_handle.get_user_by_email(us_email)
    obj = ContractEventTeam.objects.filter(
        contract__id=contract_id, user__email=us_email
    )

    if obj:
        raise Exception("User is already member of a team")

    ContractEventTeam.objects.create(contract=contract, user=user, role=role)


def update_user_in_team(contract_id, user_email, rolle):
    event_team_obj = ContractEventTeam.objects.get(
        contract__id=contract_id, user__email=user_email
    )
    if event_team_obj.role != rolle:
        event_team_obj.role = rolle
        event_team_obj.save()


def delete_user_from_team(contract_id, user_email):
    ContractEventTeam.objects.get(
        contract__id=contract_id, user__email=user_email
    ).delete()


def create_rental_product(name, picture):
    return ContractRentalProducts.objects.create(name=name, picture=picture)


def update_rental_product(name, picture, product):

    if not (
        name == product.rental_products.name
        and picture == product.rental_products.picture
    ):
        print("hee")
        product.rental_products.name = name
        if picture:
            product.rental_products.picture = picture
        product.rental_products.save()

    return product.rental_products


def add_event_rental_product(contract_id, rental_product, price, count):
    contract = handle_contract.get_contract_artist_by_id(contract_id)

    CompanyContractRentalProduct.objects.create(
        contract=contract, rental_products=rental_product, price=price, count=count
    )


def update_event_rental_product(product, rental_product, price, count):
    product.rental_products = rental_product
    product.price = price
    product.count = count
    product.save()


def get_event_products(contract_id):

    event_prod_obj = CompanyContractRentalProduct.objects.filter(
        contract__id=contract_id
    )
    if event_prod_obj:
        return event_prod_obj.first().products.all()
    return CompanyContractOneProduct.objects.filter(id__lt=0)


def delete_event_product(product_id, contract_id):

    contr_products_obj = CompanyContractRentalProduct.objects.get(
        contract__id=contract_id
    )

    product = CompanyContractOneProduct.objects.get(pk=product_id)
    product.product.in_stock += product.count
    product.product.save()
    product.delete()

    if contr_products_obj.products.count() < 1:
        contr_products_obj.delete()


def get_event_product_by_id(product_id):
    return CompanyContractRentalProduct.objects.get(pk=product_id)


def validate_product(post):
    return all([post.get("name"), post.get("price"), post.get("count")])


# def get_all_events():
#     event_ids = [el.contract.id for el in ContractEventTeam.objects.all()]
#     return Contract.objects.filter(id__in=event_ids)


def get_event_team_by_id(event_team_id):
    return ContractEventTeam.objects.get(pk=event_team_id)


def delete_event_team(event_team_id):
    get_event_team_by_id(event_team_id).delete()


# def get_event_artist_by_id(event_artist_id):
#     return EventArtists.objects.get(pk=event_artist_id)


# def delete_event_artist(event_artist_id):
#     get_event_artist_by_id(event_artist_id).delete()


def get_rental_product_by_id(rental_product_id):
    return ContractRentalProducts.objects.get(pk=rental_product_id)


def delete_rental_product(rental_product_id):
    get_rental_product_by_id(rental_product_id).delete()


def get_event_rental_product_by_id(event_product_id):
    return CompanyContractRentalProduct.objects.get(pk=event_product_id)


def delete_event_rental_product(event_product_id):
    get_event_rental_product_by_id(event_product_id).delete()


def get_event_time_clock(contract):
    event_time_clock_obj = ContractTimeClock.objects.filter(contract=contract)
    if not event_time_clock_obj:
        return None

    event_time_clock = event_time_clock_obj.first()
    return event_time_clock.day_schedule.all()


def get_or_create_contract_clock(contract_id):
    contract = handle_contract.get_contract_artist_by_id(contract_id)
    return ContractTimeClock.objects.get_or_create(contract=contract)


def add_clock_to_event_clock(contract_time_clock, time_clock):
    contract_time_clock.day_schedule.add(time_clock)


def remove_clock_to_event_clock(contract_time_clock, time_clock_id):
    time_clock = TimeClock.objects.get(id=time_clock_id)
    contract_time_clock.day_schedule.remove(time_clock)


def get_time_clock(id):
    return TimeClock.objects.get(id=id)


def is_time_fittable(event_id, start_time, end_time, time_clock_id):
    contract_clock_time = ContractTimeClock.objects.get(
        contract__id=event_id
    ).day_schedule.all()
    time_clock = get_time_clock(time_clock_id)
    index_in_all = list(contract_clock_time).index(
        time_clock
    )  # index current clock in all clocks
    previous_index = index_in_all - 1

    if previous_index >= 0:
        previous_clock = list(contract_clock_time)[previous_index]
        if previous_clock.end_time > start_time:
            print("here1")
            return True
    next_index = index_in_all + 1
    if next_index < len(list(contract_clock_time)):
        next_clock = list(contract_clock_time)[next_index]
        if next_clock.start_time < end_time:
            print("here2")
            return True


def artist_user_team(artist):
    user_ids = [el.access.id for el in ArtistAccess.objects.filter(artist=artist)]
    return [(el, el) for el in User.objects.filter(id__in=user_ids)]


def artist_user_team_queryset(artist):
    user_ids = [el.access.id for el in ArtistAccess.objects.filter(artist=artist)]
    return User.objects.filter(id__in=user_ids)


def get_artist_event_team(contract):
    return ArtistTeamEvent.objects.filter(contract=contract)


def add_event_artist_team(contract, artist_team):
    event_team_obj = ArtistTeamEvent.objects.get_or_create(contract=contract)[0]
    for el in artist_team:
        event_team_obj.artist_team.add(User.objects.get(email=el))


def get_all_event_artist_team(contract):
    event_artist_team_obj = get_artist_event_team(contract)
    if event_artist_team_obj:
        return event_artist_team_obj.first().artist_team.all()


def edit_event_artist_team(contract, artist_users_team):
    if not bool(artist_users_team.strip()):
        users_ids = []
    else:
        users_ids = artist_users_team.split("_")
    event_artist_team_obj = get_artist_event_team(contract).first()
    print(bool(artist_users_team.strip()))
    new_users_team = User.objects.filter(id__in=users_ids)
    event_artist_team_obj.artist_team.set(new_users_team)
    event_artist_team_obj.save()


# def handle_artist_user_permission(contract, event_artist):
#     users_in_team = ContractEventTeam.objects.filter(contract=contract)
#     for us in users_in_team:
#         if not ArtistAccess.objects.filter(artist=event_artist.artist, access=us.user):
#             ArtistAccess.objects.create(
#                 artist=event_artist.artist, access=us.user, admin=False
#             )


# def handle_artist_user_permission_in_team(event, user):
#     events_artists =EventArtists.objects.filter(event=event)
#     for artist in events_artists:
#         if not ArtistAccess.objects.filter(artist=artist, access=user):
#             ArtistAccess.objects.create(artist=artist, access=user, admin=False)


def confirm_product(contract_id):
    contract_products_obj = CompanyContractRentalProduct.objects.get(
        contract__id=contract_id
    )
    contract_products_obj.confirmed = True
    contract_products_obj.save()


def delete_all_expired_products(products):
    for event_products_contracts in products:
        for elem in event_products_contracts.products.all():
            elem.product.in_stock += elem.count
            elem.product.save()
            elem.delete()


def get_company_products(contract):

    past_products_for_past_products = CompanyContractRentalProduct.objects.filter(
        contract__date__lt=date.today()
    )
    print(past_products_for_past_products)
    delete_all_expired_products(past_products_for_past_products)

    try:
        c_rental_products = CompanyRentalProduct.objects.filter(
            company=contract.company
        )
        prod_ids = [
            y.id for x in c_rental_products for y in x.products.filter(in_stock__gte=1)
        ]
        return CRentalProduct.objects.filter(id__in=prod_ids)
    except Exception as err:
        print(err)
        return []


def get_product_aval_count(product, event):
    in_stock = product.in_stock
    all_contracts_for_same_date = Contract.objects.filter(date=event.date)
    for elem in all_contracts_for_same_date:
        c_c_product = CompanyContractRentalProduct.objects.filter(contract=elem)
        if c_c_product:
            for y in c_c_product.first().products.all():
                pass

    return in_stock


def get_c_c_product(product_id):
    return CompanyContractOneProduct.objects.get(pk=product_id)


def get_c_product_one(product_id):
    return CompanyContractOneProduct.objects.get(pk=product_id)


def check_prod_exists_in_contr_products(contract, product):
    contract_products_obj = CompanyContractRentalProduct.objects.get(contract=contract)
    contract_product = contract_products_obj.products.filter(product__id=product.id)
    return contract_product.first() if contract_product else None


def get_all_products_price(event_products):
    return sum(el.total_price for el in event_products)


def get_all_products_count(event_products):
    return sum(el.count for el in event_products)
