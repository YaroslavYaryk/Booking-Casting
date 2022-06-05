from django.shortcuts import render
from customer.services import handle_customer
from .forms import (
    ContractArtistForm,
    ContractForm,
    ContractArtistEditForm,
    UserContractArtistForm,
    UserContractArtistEditForm,
)
from venue.services import handle_venue
from event.services import handle_event
from django.contrib import messages
from django.urls.base import reverse
from django.http import HttpResponseRedirect
from .services import handle_contract, constants, static_function
from users.services import user_handle
from artist.services import user_artists, constants as art_constants
from datetime import datetime


def create_contract(request, customer_id):

    customer = handle_customer.get_customer_by_id(customer_id)
    aval_arists = handle_customer.get_avaluable_artists(customer)
    companies = handle_event.get_company_queryset(request.user)
    venues = handle_event.get_venue_queryset(request.user)

    if request.method == "POST":
        form = ContractArtistForm(aval_arists, companies, venues, request.POST)

        if form.is_valid():
            contract_obj = form.save()
            contract_obj.customer = customer
            contract_obj.save()
            handle_customer.add_team_peermission_to_change_contract_details(
                contract_obj
            )
            return HttpResponseRedirect(
                reverse(
                    "customer_get_contract",
                    kwargs={
                        "contract_id": contract_obj.id,
                    },
                )
            )

    else:
        form = ContractArtistForm(aval_arists, companies, venues)

    context = {"form": form, "customer": customer}
    return render(request, "contract/make_contract.html", context=context)


def get_contract(request, contract_id):

    cotract_artist = handle_contract.get_contract_artist_by_id(contract_id)
    rendered_template = handle_contract.rerender_contract(cotract_artist)
    # return rendered_template
    if request.method == "POST":
        form = ContractForm(rendered_template, request.POST)
        if form.is_valid():
            cotract_artist.contract = form.cleaned_data["contract"]
            cotract_artist.save()
            return HttpResponseRedirect(
                reverse(
                    "preview_artist_contract", kwargs={"contract_id": cotract_artist.id}
                )
            )
    else:
        form = ContractForm(rendered_template)

    context = {"form": form, "contract": cotract_artist, "delete": True}

    return render(request, "contract/contract.html", context)


def preview_artist_contract(request, contract_id):
    contract_artist = handle_contract.get_contract_artist_by_id(contract_id)
    contract = handle_contract.rerender_contract(
        contract_artist, constants.PREVIEW_CONTRACT
    )

    return render(
        request,
        "contract/preview_contract.html",
        {
            "artist": contract_artist,
            "contract": contract_artist.contract,
            "company_image_link": static_function.get_company_image_link(
                contract_artist.company.icon.url
            ),
            "customer_contact_phone": handle_customer.get_customer_contact(
                contract_artist.customer
            ).phone,
            "customer_email": handle_customer.get_customer_contact(
                contract_artist.customer
            ).email,
        },
    )


def save_artist_contract_data(
    request, event_artist_id, date, honorar, payment_methods, comment, page_heights
):
    contract_artist = handle_contract.get_contract_artist_by_id(event_artist_id)
    contract_artist.date = date
    contract_artist.price = honorar
    contract_artist.payment_methods = payment_methods
    contract_artist.comment = comment

    try:
        contract_artist.contract_pdf_url = handle_contract.create_pdf_contract(
            contract_artist, page_heights
        )
        contract_artist.save()
    except Exception as err:
        raise err
        messages.error(request, "something went wrong")

    return HttpResponseRedirect(
        reverse(
            "customer_details",
            kwargs={
                "customer_id": contract_artist.customer.id,
            },
        )
    )


def get_visible_contracted_artists(request, customer_id, date):

    customer = handle_customer.get_customer_by_id(customer_id)
    artists = handle_contract.get_contracted_artists(customer, date)
    context = {
        "artists": artists,
        "customer": customer,
        "hidden": False,
        "today_date": date,
        "today_today": str(datetime.today().date()),
        "week_days_list": user_artists.get_week_days_list(
            datetime.strptime(date, "%Y-%m-%d").date(),
            art_constants.week_names_count[
                datetime.strptime(date, "%Y-%m-%d").date().strftime("%A")
            ],
        ),
    }

    return render(request, "contract/artists_list.html", context=context)


def cancel_contract(request, contract_id, redirect_link):

    try:
        customer_id = handle_contract.delete_contract(contract_id)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    return handle_contract.get_responce_redirect(customer_id, redirect_link)


def edit_contract(request, contract_id):

    if not handle_contract.user_has_access_to_customer(contract_id, request.user):
        return render(request, "dashboard/page_blocked.html")

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    customer = handle_customer.get_customer_by_id(contract.customer.id)
    companies = handle_event.get_company_queryset(request.user)
    venues = handle_event.get_venue_queryset(request.user)

    if request.method == "POST":
        form = ContractArtistEditForm(
            companies,
            venues,
            request.POST,
            instance=contract,
        )

        if form.is_valid():
            contr = form.save()
            contr.customer = customer
            contr.artist = contract.artist
            contr.contract = handle_contract.rerender_contract(contr)
            contr.save()
            return HttpResponseRedirect(
                reverse("preview_artist_contract", kwargs={"contract_id": contract.id})
            )

    else:
        form = ContractArtistEditForm(companies, venues, instance=contract)

    context = {"form": form, "customer": customer, "artist": contract.artist}
    return render(request, "contract/edit_contract.html", context=context)


def get_contract_view(request, contract_id):

    rendered_template = handle_contract.get_rendered_contract(contract_id)
    cotract_artist = handle_contract.get_contract_artist_by_id(contract_id)
    # return rendered_template
    if request.method == "POST":
        form = ContractForm(rendered_template, request.POST)
        if form.is_valid():
            cotract_artist.contract = form.cleaned_data["contract"]
            cotract_artist.save()
            return HttpResponseRedirect(
                reverse(
                    "preview_artist_contract", kwargs={"contract_id": cotract_artist.id}
                )
            )
    else:
        form = ContractForm(rendered_template)

    context = {"form": form, "contract": cotract_artist, "delete": False}

    return render(request, "contract/contract.html", context)


# def preview_artist_contract_view(request, contract_id):
#     contract_artist = handle_contract.get_contract_artist_by_id(contract_id)

#     return render(
#         request,
#         "contract/preview_contract.html",
#         {"artist": contract_artist, "to_customer": True},
#     )


def hide_contract(request, contract_id):

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.hide_contract(contract)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_all_contracted_artists",
            kwargs={
                "customer_id": contract.customer.id,
                "date": str(datetime.today().date()),
            },
        )
    )


def unhide_contract(request, contract_id):
    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.unhide_contract(contract)
    except Exception as err:
        print(err)
        messages.error(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_hidden_contracts_list", kwargs={"customer_id": contract.customer.id}
        )
    )


def get_hidden_contracts_list(request, customer_id):

    customer = handle_customer.get_customer_by_id(customer_id)
    contracts = handle_contract.get_hidden_contracts(customer)

    context = {
        "hidden": True,
        "artists": contracts,
        "customer": customer,
        "today_today": str(datetime.today().date()),
    }

    return render(request, "contract/artists_list.html", context=context)


def get_visible_contracts_for_user(request, user_id):

    user = user_handle.get_user_by_id(user_id)

    try:
        contracts = handle_contract.get_contracts_for_user(user)
    except Exception as err:
        print(err)
        messages.error(request, "Something went wrong")

    return render(
        request,
        "contract/contracts_for_user.html",
        {"contracts": contracts, "hidden": False},
    )


def get_hidden_contracts_for_user(request, user_id):

    user = user_handle.get_user_by_id(user_id)

    try:
        contracts = handle_contract.get_contracts_for_user(user, False)
    except Exception as err:
        print(err)
        messages.error(request, "Something went wrong")

    return render(
        request,
        "contract/contracts_for_user.html",
        {"contracts": contracts, "hidden": True},
    )


def customer_create_contract_from_user(request, user_id):

    user = user_handle.get_user_by_id(user_id)

    customers = handle_event.get_customer_queryset(user)
    aval_arists = handle_event.get_artist_queryset(user)
    companies = handle_event.get_company_queryset(user)
    venues = handle_event.get_venue_queryset(user)

    if request.method == "POST":
        form = UserContractArtistForm(
            customers, aval_arists, companies, venues, request.POST
        )

        if form.is_valid():

            contract_obj = form.save()

            handle_customer.add_team_peermission_to_change_contract_details(
                contract_obj
            )
            return HttpResponseRedirect(
                reverse(
                    "customer_get_contract",
                    kwargs={
                        "contract_id": contract_obj.id,
                    },
                )
            )
        else:
            pass
            # messages.error(request, form.errors.as_text)

    else:
        form = UserContractArtistForm(customers, aval_arists, companies, venues)

    context = {
        "form": form,
    }
    return render(request, "contract/user_make_contract.html", context=context)


def user_edit_contract(request, contract_id):

    if not handle_contract.user_has_access_to_customer(contract_id, request.user):
        return render(request, "dashboard/page_blocked.html")

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    customer = handle_customer.get_customer_by_id(contract.customer.id)
    companies = handle_event.get_company_queryset(request.user)
    venues = handle_event.get_venue_queryset(request.user)

    if request.method == "POST":
        form = ContractArtistEditForm(
            companies,
            venues,
            request.POST,
            instance=contract,
        )

        if form.is_valid():
            contr = form.save()
            contr.customer = customer
            contr.artist = contract.artist
            contr.contract = handle_contract.rerender_contract(contr)
            contr.save()
            return HttpResponseRedirect(
                reverse("preview_artist_contract", kwargs={"contract_id": contract.id})
            )

    else:
        form = ContractArtistEditForm(companies, venues, instance=contract)

    context = {"form": form, "customer": customer, "artist": contract.artist}
    return render(request, "contract/user_edit_contract.html", context=context)


def hide_contract_from_user(request, contract_id):

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.hide_contract(contract)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse("get_visible_contracts_for_user", kwargs={"user_id": request.user.id})
    )


def unhide_contract_from_user(request, contract_id):
    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.unhide_contract(contract)
    except Exception as err:
        print(err)
        messages.error(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse("get_hidden_contracts_for_user", kwargs={"user_id": request.user.id})
    )
