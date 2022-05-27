from os import access
from contract.models import Contract
from jinja2 import Template
from .constants import BASE_CONTRACT, EDIT_CONTRACT, BASE_FIELD_LENGTH
from customer.models import CustomerAccess, CustomerContacts
from django.urls.base import reverse
from django.http import HttpResponseRedirect
import pdfkit
from decouple import config


def get_contract_artist_by_id(id):
    return Contract.objects.get(id=id)


def get_company_image(link):
    return f"""
        <img style="position:absolute; top:20px; right:50px;" width="350" height="150" src="{config('HOST')}:{config('PORT')}{link}"  alt="" >
    """


even_products = """ 
    {% for product in rental_products %}
                <p>{{product.rental_products.name}} ({{product.count}}) - {{product.price}}</p>
              {% endfor %}
"""


def get_rendered_contract(request, event_artist_id):

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
    return rendered_contract


def get_contracted_artists(customer):
    return Contract.objects.filter(customer=customer)


def delete_contract(contract_id):

    contract = get_contract_artist_by_id(contract_id)
    customer_id = contract.customer.id
    contract.delete()

    return customer_id


def divide_payment_methods(text, length):
    if length < 30:
        first_row = text
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

    length2 = len(" ".join([el for el in text.split()[index1:]]))
    res2 = divide_payment_methods(text.split()[index1:], length2)
    p_methods_two = res2[0]
    return " ".join([el for el in p_methods_one]), " ".join(
        [el for el in p_methods_two]
    )


def rerender_contract(contr):

    method_payment = get_payment_methods_rows(contr.payment_methods)

    customer_contact = CustomerContacts.objects.get(customer=contr.customer)
    contract = Template(EDIT_CONTRACT)
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
            comment=contr.comment,
            cusomer_date_of_birth=customer_contact.birthdate,
            trim_blocks=True,
            lstrip_blocks=True,
            customer_contact_phone=customer_contact.phone,
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
            comment=contr.comment,
            cusomer_date_of_birth=customer_contact.birthdate,
            trim_blocks=True,
            lstrip_blocks=True,
            customer_contact_phone=customer_contact.phone,
        )
    return rendered_contract


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


def create_pdf_contract(contract_artist):

    contract = rerender_contract(contract_artist)
    pdfkit.from_string(contract, "sample.pdf")
