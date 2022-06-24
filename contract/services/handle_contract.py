from datetime import datetime, timedelta
from company.models import CompanyAccess
from artist.models import ArtistAccess
from venue.models import VenueAccess
from contract.models import Contract, ContractEventTeam
from jinja2 import Template
from .constants import BASE_CONTRACT, EDIT_CONTRACT, PDF_CONTRACT, additinal_staff_list
from customer.models import CustomerAccess, CustomerContacts
from django.urls.base import reverse
from django.http import HttpResponseRedirect
import pdfkit
from django.template.loader import render_to_string
from django.utils.text import slugify
from .static_function import get_company_image
import time
import json
from artist.models import ArtistBusyDates


def get_contract_artist_by_id(id):
    return Contract.objects.get(id=id)


aditional_staff_template = """
        <table border="0"  cellpadding="1" cellspacing="1" style="width:1000px">
            <tbody>
                {% for elem in additinal_staff_list %}
                    <tr>
                        {% if to_pdf %}
                            <td>{{elem}}&nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp;</td>
                        {% else %}
                            <td>{{elem}}&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp;</td>
                        {% endif %}
                        {% if elem in contract_add_staff %}
                            <td><u>inkludert</u></td>
                        {% else %}
                            <td><u>ihht. Rider</u></td>
                        {% endif %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    """


even_products = """ 
    {% for product in rental_products %}
                <p>{{product.rental_products.name}} ({{product.count}}) - {{product.price}}</p>
              {% endfor %}
"""


def get_rendered_contract(event_artist_id):

    event_artist = get_contract_artist_by_id(event_artist_id)
    customer_contact = CustomerContacts.objects.get(customer=event_artist.customer)
    if event_artist.contract:
        return event_artist.contract

    contract = Template(BASE_CONTRACT)

    if event_artist.company:
        rendered_contract = contract.render(
            company_image=get_company_image(event_artist.company.icon.url),
            artist=event_artist.artist,
            company=event_artist.company,
            org_number=event_artist.customer.organization_number,
            cust_cont_full_name=event_artist.customer.name,
            venue=event_artist.venue,
            customer=event_artist.customer,
            customer_email=customer_contact.email,
            cusomer_date_of_birth=customer_contact.birthdate,
            trim_blocks=True,
            lstrip_blocks=True,
            customer_contact_phone=customer_contact.phone,
        )
    else:
        rendered_contract = contract.render(
            artist=event_artist.artist,
            company=event_artist.company,
            org_number=event_artist.customer.organization_number,
            cust_cont_full_name=event_artist.customer.name,
            venue=event_artist.venue,
            customer=event_artist.customer,
            customer_email=customer_contact.email,
            cusomer_date_of_birth=customer_contact.birthdate,
            trim_blocks=True,
            lstrip_blocks=True,
            customer_contact_phone=customer_contact.phone,
        )
    print(rendered_contract)
    return rendered_contract


def get_contracted_artists(customer, date):
    return Contract.objects.filter(customer=customer, visible=True, date=date)


def get_hidden_contracts(customer):
    print(Contract.objects.filter(customer=customer, visible=False))
    return Contract.objects.filter(customer=customer, visible=False)


def delete_contract(contract_id):

    contract = get_contract_artist_by_id(contract_id)
    customer_id = contract.customer.id
    contract.delete()

    return customer_id


def divide_payment_methods(text, length):
    first_row = text
    if length < 30:
        index = -1
    else:

        summ = 0
        index = 0
        for i in range(len(text)):
            summ += len(text[i]) + 1
            if summ > 30:
                summ -= len(text[i]) - 1
                first_row = " ".join([el for el in text[:i]])
                index = i
                return first_row, index
    return first_row, index


def get_payment_methods_rows(text):

    res1 = divide_payment_methods(text.split(), len(text))
    index1 = res1[1]
    p_methods_one = res1[0]
    if index1 != -1:
        length2 = len(" ".join([el for el in text.split()[index1:]]))
        res2 = divide_payment_methods(text.split()[index1:], length2)
        p_methods_two = res2[0]
    else:
        p_methods_two = ""
    if p_methods_one and p_methods_two:

        return (
            "".join([el for el in p_methods_one]),
            "".join([el for el in p_methods_two]) or " ",
        )

    return (
        " ".join([el for el in p_methods_one]),
        " ".join([el for el in p_methods_two]) or " ",
    )


def get_comment_or_none(comment):
    if not all([i == " " for i in comment]):
        return comment
    return ""


def rerender_contract(contr, contract_template=EDIT_CONTRACT, to_pdf=False):

    method_payment = get_payment_methods_rows(contr.payment_methods)

    customer_contact = CustomerContacts.objects.get(customer=contr.customer)

    contract_aditional_staff_template = Template(aditional_staff_template)

    contract = Template(contract_template)
    if contr.company:
        rendered_contract = contract.render(
            company_image=get_company_image(contr.company.icon.url),
            artist=contr.artist,
            company=contr.company,
            org_number=contr.customer.organization_number,
            cust_cont_full_name=contr.customer.name,
            venue=contr.venue,
            customer=contr.customer,
            customer_email=customer_contact.email,
            contract=contr,
            p_methods_one=method_payment[0],
            p_methods_two=method_payment[1],
            comment=get_comment_or_none(contr.comment),
            cusomer_date_of_birth=customer_contact.birthdate,
            trim_blocks=True,
            lstrip_blocks=True,
            customer_contact_phone=customer_contact.phone,
            contract_add_staff=contract_aditional_staff_template.render(
                additinal_staff_list=additinal_staff_list,
                contract_add_staff=contr.aditional_staff,
                to_pdf=to_pdf,
            ),
        )
    else:
        rendered_contract = contract.render(
            artist=contr.artist,
            company=contr.company,
            org_number=contr.customer.organization_number,
            cust_cont_full_name=contr.customer.name,
            venue=contr.venue,
            customer=contr.customer,
            customer_email=customer_contact.email,
            contract=contr,
            p_methods_one=method_payment[0],
            p_methods_two=method_payment[1],
            comment=get_comment_or_none(contr.comment),
            cusomer_date_of_birth=customer_contact.birthdate,
            trim_blocks=True,
            lstrip_blocks=True,
            customer_contact_phone=customer_contact.phone,
            contract_add_staff=contract_aditional_staff_template.render(
                additinal_staff_list=additinal_staff_list,
                contract_add_staff=customer_contact.aditional_staff,
            ),
        )
    return rendered_contract


# def get_header_for_page(contract):
#     return """
#         <p>
# 			{% if company %}
# 			{{company.name}}<br />
# 			{{company.address}}<br />
# 			{{company.zip_code}}&nbsp;{{company.city}}<br />
# 			{% endif %}
# 			Tlf: {{customer_contact_phone}}<br />
# 			E-mail:{{customer_email}}
# 		</p>

# 		<p>{{company_image}}</p>

# 	<p>&nbsp;</p>
#     """


def user_has_access_to_customer(contract_id, user):
    contract = get_contract_artist_by_id(contract_id)
    customer = contract.customer
    return CustomerAccess.objects.filter(customer=customer, access=user, admin=True)


def get_responce_redirect(customer_id, redirect_link):
    if not redirect_link == "customer":
        return HttpResponseRedirect(
            reverse("get_all_contracted_artists", kwargs={"customer_id": customer_id})
        )
    return HttpResponseRedirect(
        reverse("customer_details", kwargs={"customer_id": customer_id})
    )


def create_pdf_contract(contract_artist, page_heights):

    a, b, c, d = page_heights.split("_")

    contract = rerender_contract(contract_artist, PDF_CONTRACT, to_pdf=True)

    context = {"contract": contract, "first": a, "second": b, "third": c, "forth": d}
    t = render_to_string("contract/contract_to_pdf.html", context)
    pdfkit.from_string(
        t,
        f"media/contracts/{slugify(contract_artist.customer.name)}_{slugify(contract_artist.artist.name)}.pdf",
    )
    return f"/media/contracts/{slugify(contract_artist.customer.name)}_{slugify(contract_artist.artist.name)}.pdf"


def hide_contract(contract):

    contract.visible = False
    contract.save()


def unhide_contract(contract):
    contract.visible = True
    contract.save()


def get_contracts_for_user(user, visible=True):
    customer_ids = [
        el.customer.id for el in CustomerAccess.objects.filter(access=user, admin=True)
    ]
    contract_ids = [
        el.contract.id for el in ContractEventTeam.objects.filter(user=user)
    ]

    return Contract.objects.filter(id__in=contract_ids, visible=visible)


def artist_taken_for_date(artist, date, contract_id):
    return artist.contract_set.filter(date=date).exclude(id=contract_id)


def handle_artist_taken(contract_obj, edit=False):

    response = ""

    if artist_taken_for_date(contract_obj.artist, contract_obj.date, contract_obj.id):

        response = HttpResponseRedirect(
            reverse(
                "create_contract_with_errors",
                kwargs={
                    "contract_id": contract_obj.id,
                },
            )
        )
        if edit:
            response.set_cookie("from_edit", True)
        response.set_cookie(
            "error_message", "This artist already has event for this date"
        )
    return response


def venue_taken_for_date(venue, date, contract_id):
    return venue.contract_set.filter(date=date).exclude(id=contract_id)


def handle_venue_taken(contract_obj, edit=False):
    response = ""
    if venue_taken_for_date(contract_obj.venue, contract_obj.date, contract_obj.id):
        response = HttpResponseRedirect(
            reverse(
                "create_contract_with_errors",
                kwargs={
                    "contract_id": contract_obj.id,
                },
            )
        )
        if edit:
            response.set_cookie("from_edit", True)
        response.set_cookie(
            "error_message", "This venue already has event for this date"
        )
    return response


def get_upcoming_events(customer, date):
    date_today_datetime = datetime.strptime(date, "%Y-%m-%d").date()
    date_to = str(date_today_datetime + timedelta(days=20))
    return Contract.objects.filter(
        customer=customer, date__gte=date, date__lte=date_to, visible=True
    )


def handle_artist_taken_from_user(contract_obj, edit=False):
    response = ""
    if artist_taken_for_date(contract_obj.artist, contract_obj.date, contract_obj.id):

        response = HttpResponseRedirect(
            reverse(
                "create_contract_with_errors_from_user",
                kwargs={
                    "contract_id": contract_obj.id,
                },
            )
        )
        if edit:
            response.set_cookie("from_edit_user", True)
        response.set_cookie(
            "error_message_from_user", "This artist already has event for this date"
        )
    return response


def handle_venue_taken_from_user(contract_obj, edit=False):
    response = ""
    if venue_taken_for_date(contract_obj.venue, contract_obj.date, contract_obj.id):
        response = HttpResponseRedirect(
            reverse(
                "create_contract_with_errors_from_user",
                kwargs={
                    "contract_id": contract_obj.id,
                },
            )
        )
        if edit:
            response.set_cookie("from_edit_user", True)
        response.set_cookie(
            "error_message_from_user", "This venue already has event for this date"
        )
    return response


def add_user_to_event_contract_team(contract_id, user, role):
    contract = get_contract_artist_by_id(contract_id)
    ContractEventTeam.objects.get_or_create(contract=contract, user=user, role=role)


def add_perm_to_event_to_all_users_of_artist(artist, contract):
    artist_access_obj = ArtistAccess.objects.filter(artist=artist)
    for elem in artist_access_obj:
        event_team_user = ContractEventTeam.objects.filter(
            contract=contract, user=elem.access
        )
        if not event_team_user:
            if elem.admin:
                ContractEventTeam.objects.create(
                    contract=contract, user=elem.access, role="admin"
                )
            else:
                ContractEventTeam.objects.create(
                    contract=contract, user=elem.access, role="user"
                )


def add_perm_to_event_to_all_users_of_customer(customer, contract):
    customer_access_obj = CustomerAccess.objects.filter(customer=customer)
    for elem in customer_access_obj:
        event_team_user = ContractEventTeam.objects.filter(
            contract=contract, user=elem.access
        )
        if not event_team_user:
            if elem.admin:
                ContractEventTeam.objects.create(
                    contract=contract, user=elem.access, role="admin"
                )
            else:
                ContractEventTeam.objects.create(
                    contract=contract, user=elem.access, role="user"
                )


def add_perm_to_event_to_all_users_of_venue(venue, contract):
    venue_access_obj = VenueAccess.objects.filter(venue=venue)
    for elem in venue_access_obj:
        event_team_user = ContractEventTeam.objects.filter(
            contract=contract, user=elem.access
        )
        if not event_team_user:
            ContractEventTeam.objects.create(
                contract=contract, user=elem.access, role="user"
            )


def add_perm_to_event_company_creator(company, contract):

    company_access_obj = CompanyAccess.objects.filter(company=company)

    for elem in company_access_obj:
        event_team_user = ContractEventTeam.objects.filter(
            contract=contract, user=elem.access
        )
        if not event_team_user:
            if elem.admin:
                ContractEventTeam.objects.create(
                    contract=contract, user=elem.access, role="admin"
                )
            else:
                ContractEventTeam.objects.create(
                    contract=contract, user=elem.access, role="user"
                )


def add_permission_participants_to_contract_event(contract):
    artist = contract.artist
    customer = contract.customer
    venue = contract.venue
    company = contract.company
    print("here")

    add_perm_to_event_to_all_users_of_artist(artist, contract)
    add_perm_to_event_to_all_users_of_customer(customer, contract)
    add_perm_to_event_to_all_users_of_venue(venue, contract)
    add_perm_to_event_company_creator(company, contract)


def add_perm_to_company_to_all_users_of_artist(artist, company):
    artist_access_obj = ArtistAccess.objects.filter(artist=artist)
    for elem in artist_access_obj:
        event_team_user = CompanyAccess.objects.filter(
            company=company, access=elem.access
        )
        if not event_team_user:
            CompanyAccess.objects.create(
                company=company, access=elem.access, admin=False
            )


def add_perm_to_company_to_all_users_of_customer(customer, company):
    customer_access_obj = CustomerAccess.objects.filter(customer=customer)
    for elem in customer_access_obj:
        event_team_user = CompanyAccess.objects.filter(
            company=company, access=elem.access
        )
        if not event_team_user:
            CompanyAccess.objects.create(
                company=company, access=elem.access, admin=False
            )


def add_perm_to_company_to_all_users_of_venue(venue, company):
    venue_access_obj = VenueAccess.objects.filter(venue=venue)
    for elem in venue_access_obj:
        event_team_user = CompanyAccess.objects.filter(
            company=company, access=elem.access
        )
        if not event_team_user:
            CompanyAccess.objects.create(
                company=company, access=elem.access, admin=False
            )


def add_contract_members_access(contract_artist):
    artist = contract_artist.artist
    customer = contract_artist.customer
    venue = contract_artist.venue
    company = contract_artist.company

    add_perm_to_company_to_all_users_of_artist(artist, company)
    add_perm_to_company_to_all_users_of_customer(customer, company)
    add_perm_to_company_to_all_users_of_venue(venue, company)


def is_allowed_to_change_contract(contract_id, user):
    print(ContractEventTeam.objects.filter(contract__id=contract_id, user=user))
    return ContractEventTeam.objects.get(
        contract__id=contract_id, user=user, role="admin"
    )


def get_artist_taken_dates(contract_artist):
    artist = contract_artist.artist

    return json.dumps(
        [
            int(time.mktime(el.date.timetuple())) * 1000
            for el in Contract.objects.filter(artist=artist).exclude(
                id=contract_artist.id
            )
        ]
    )


def get_venues_taken_dates(contract_artist):
    venue = contract_artist.venue
    print(
        json.dumps(
            [
                time.mktime(el.date.timetuple()) * 1000
                for el in Contract.objects.filter(venue=venue).exclude(
                    id=contract_artist.id
                )
            ]
        )
    )
    return json.dumps(
        [
            time.mktime(el.date.timetuple()) * 1000
            for el in Contract.objects.filter(venue=venue).exclude(
                id=contract_artist.id
            )
        ]
    )


def get_contract_artist_date(contract_artist):
    customer = contract_artist.customer
    artist = contract_artist.artist
    return json.dumps(
        [
            time.mktime(el.date.timetuple()) * 1000
            for el in Contract.objects.filter(artist=artist, customer=customer).exclude(
                id=contract_artist.id
            )
        ]
    )


def add_date_to_user_busy(contract_artist):
    company_name = contract_artist.company.name

    ArtistBusyDates.objects.create(
        artist=contract_artist.artist,
        start_date=contract_artist.date,
        end_date=contract_artist.date,
        busy_action=f"Event in {company_name}",
    )
