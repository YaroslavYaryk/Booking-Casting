from os import access
from contract.models import Contract
from jinja2 import Template
from .constants import BASE_CONTRACT, EDIT_CONTRACT, PDF_CONTRACT, additinal_staff_list
from customer.models import CustomerAccess, CustomerContacts
from django.urls.base import reverse
from django.http import HttpResponseRedirect
import pdfkit
from django.template.loader import render_to_string
from django.utils.text import slugify
from .static_function import get_company_image


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
        return "".join([el for el in p_methods_one]), "".join(
            [el for el in p_methods_two]
        )
    return " ".join([el for el in p_methods_one]), " ".join(
        [el for el in p_methods_two]
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

    return Contract.objects.filter(customer__id__in=customer_ids, visible=visible)
