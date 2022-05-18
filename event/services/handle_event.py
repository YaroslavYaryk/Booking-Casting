from artist.models import Artist, ArtistAccess
from artist.services import user_artists
from company.models import Company
from customer.models import Customer, CustomerAccess
from event.models import (Event, EventArtists, EventRentalProducts, EventTeam,
                          RentalProducts)
from jinja2 import Template
from users.models import User
from users.services import user_handle
from venue.models import Venue, VenueAccess


def get_event_for_user(user):
    return EventTeam.objects.filter(user=user)

def get_event_by_id(id):
    return Event.objects.get(pk=id)

def delete_event(event_id):
    get_event_by_id(event_id).delete()

def get_company_queryset(user):
    return Company.objects.filter(creator=user, active=True)

def get_venue_queryset(user):
    
    my_venues =  [el.venue.email for el in VenueAccess.objects.filter(access=user)]
    return Venue.objects.filter(email__in = my_venues, active=True)


def get_customer_queryset(user):
    my_customers =  [el.customer.id for el in CustomerAccess.objects.filter(access=user)]
    return Customer.objects.filter(pk__in = my_customers, active=True)

def get_linked_text(link, id, object):
    return f""" <a style="color:black" href="../../../{link}/{id}/details/">{object}</a> """


artists = """
<ul>
    {% for obj in artists %}
        <li> <a style="color:black" href="../../../artist/{{obj.artist.id}}/">{{obj.artist.name}}</a></li>
    {% endfor %}
</ul>
"""

def get_final_contract(event_obj):
    contract = Template(event_obj.contract_template)
    customer_name = get_linked_text("customer", event_obj.customer.id, event_obj.customer.name)
    company_name = get_linked_text("company", event_obj.company.id, event_obj.company.name)
    venue_name = get_linked_text("venue", event_obj.venue.id, event_obj.venue.name)
    event_artist_object = EventArtists.objects.filter(event=event_obj)
    artists_objs = Template(artists)
    artists_display_list = artists_objs.render(artists=event_artist_object)
    return contract.render(customer=customer_name,company=company_name, venue=venue_name, artists=artists_display_list )


def add_user_to_event_team(event_id, user, role):
    event = get_event_by_id(event_id)
    EventTeam.objects.create(event=event, user=user, role=role)


def is_allowed_to_change(event_id, user):
    event = get_event_by_id(event_id)
    return EventTeam.objects.filter(event=event, user=user)


def get_users_team(event_id, user):
    event = get_event_by_id(event_id)
    return EventTeam.objects.filter(event=event).exclude(user=user)


def get_avaluable_users(event):
    taken_users = [us.user.email for us in EventTeam.objects.filter(event=event)]
    taken_users += [us.email for us in User.objects.filter(admin=True)]
    return User.objects.exclude(email__in = taken_users)


def get_my_artists(user):
    
    artist_access_obj = [el.artist.id for el in ArtistAccess.objects.filter(access=user) if el.artist.active]
    return Artist.objects.filter(id__in = artist_access_obj)

    
    
def get_active_artists(event_id):
    event = get_event_by_id(event_id)
    existing_artist_in_event = [obj.artist.id for obj in  EventArtists.objects.filter(event=event)]
    return Artist.objects.filter(active=True).exclude(id__in = existing_artist_in_event)


def get_event_artists(event_id):
    event = get_event_by_id(event_id)
    return EventArtists.objects.filter(event=event)



def delete_artist_from_event(event_id, artist_id):
    EventArtists.objects.get(event__id = event_id, artist__id = artist_id).delete()


def get_event_artist_by_id(ev_artist_id):
    return EventArtists.objects.get(pk=ev_artist_id)


def is_allowed_to_change(event_id, user):
    return EventTeam.objects.get(event__id = event_id, user=user)


def add_user_to_team(event_id, us_email, role):
    event = get_event_by_id(event_id)
    user = user_handle.get_user_by_email(us_email)
    obj = EventTeam.objects.filter(event__id = event_id, user__email = us_email)
    
    if obj:
        raise Exception("User is already member of a team")
    
    EventTeam.objects.create(event = event, user = user, role=role)


def update_user_in_team( event_id, user_email, rolle):
    event_team_obj = EventTeam.objects.get(event__id = event_id, user__email=user_email)
    if event_team_obj.role != rolle:
        event_team_obj.role = rolle
        event_team_obj.save()


def delete_user_from_team( event_id, user_email):
    EventTeam.objects.get(event__id = event_id, user__email=user_email).delete()


def create_rental_product(name, picture):
    return RentalProducts.objects.create(name=name, picture=picture)


def update_rental_product(name, picture, product):
    
    if not (name == product.rental_products.name and 
        picture == product.rental_products.picture):
        print("hee")
        product.rental_products.name = name
        if picture:
            product.rental_products.picture = picture
        product.rental_products.save()
        
    
    return product.rental_products


def add_event_rental_product(event_id, rental_product, price, count):
    event = get_event_by_id(event_id)
    
    EventRentalProducts.objects.create(event=event, rental_products=rental_product,
                                       price=price, count=count)

def update_event_rental_product(product, rental_product, price, count):
    print(rental_product.picture)
    product.rental_products = rental_product
    product.price = price
    product.count = count
    product.save()


def get_event_products(event_id):
    return EventRentalProducts.objects.filter(event__id = event_id)


def delete_event_product(product_id):
    RentalProducts.objects.get(pk=product_id).delete()


def get_event_product_by_id(product_id):
    return EventRentalProducts.objects.get(pk=product_id)


def validate_product(post):
    return all([post.get("name"), post.get("price") , post.get("count")])


def get_all_events():
    event_ids = [el.event.id for el in EventTeam.objects.all()]
    return Event.objects.filter(id__in = event_ids)


def get_event_team_by_id(event_team_id):
    return EventTeam.objects.get(pk=event_team_id)


def delete_event_team(event_team_id):
    get_event_team_by_id(event_team_id).delete()


def get_event_artist_by_id(event_artist_id):
    return EventArtists.objects.get(pk=event_artist_id)


def delete_event_artist(event_artist_id):
    get_event_artist_by_id(event_artist_id).delete()


def get_rental_product_by_id(rental_product_id):
    return RentalProducts.objects.get(pk=rental_product_id)


def delete_rental_product(rental_product_id):
    get_rental_product_by_id(rental_product_id).delete()


def get_event_rental_product_by_id(event_product_id):
    return EventRentalProducts.objects.get(pk=event_product_id)


def delete_event_rental_product(event_product_id):
    get_event_rental_product_by_id(event_product_id).delete()
