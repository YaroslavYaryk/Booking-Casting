from urllib import response
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
    aval_arists = handle_customer.get_all_artists(request.user)
    companies = handle_event.get_company_queryset(request.user)
    venues = handle_event.get_venue_queryset(request.user)

    if request.method == "POST":
        form = ContractArtistForm(aval_arists, companies, venues, request.POST)

        if form.is_valid():
            try:
                contract_obj = form.save()
                contract_obj.customer = customer
                contract_obj.save()
            except Exception as err:
                messages.error(
                    request,
                    "Contract with this customer and artist for this date already exists",
                )
                contract_obj.delete()
                # raise err
                return HttpResponseRedirect(
                    reverse(
                        "customer_create_contract",
                        kwargs={
                            "customer_id": customer_id,
                        },
                    )
                )

            handle_customer.add_team_peermission_to_change_contract_details(
                contract_obj
            )
            handle_contract.add_user_to_event_contract_team(
                contract_obj.id, request.user, "admin"
            )
            handle_contract.add_permission_participants_to_contract_event(contract_obj)
            taken_artist = handle_contract.handle_artist_taken(contract_obj)
            if taken_artist:
                return taken_artist
            taken_venue = handle_contract.handle_venue_taken(contract_obj)
            if taken_venue:
                return taken_venue
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


def create_contract_with_errors(request, contract_id):

    companies = handle_event.get_company_queryset(request.user)
    venues = handle_event.get_venue_queryset(request.user)
    contract = handle_contract.get_contract_artist_by_id(contract_id)

    form = ContractArtistEditForm(companies, venues, instance=contract)

    context = {
        "form": form,
        "customer": contract.customer,
        "artist": contract.artist,
        "error_message": request.COOKIES.get("error_message"),
        "contract_id": contract.id,
    }
    return render(request, "contract/make_contract_with_error.html", context=context)


def create_contract_with_errors_from_user(request, contract_id):

    companies = handle_event.get_company_queryset(request.user)
    venues = handle_event.get_venue_queryset(request.user)
    contract = handle_contract.get_contract_artist_by_id(contract_id)

    form = UserContractArtistEditForm(companies, venues, instance=contract)

    context = {
        "form": form,
        "customer": contract.customer,
        "artist": contract.artist,
        "error_message": request.COOKIES.get("error_message_from_user"),
        "contract_id": contract.id,
    }
    return render(
        request, "contract/make_contract_from_user_with_error.html", context=context
    )


def get_contract(request, contract_id):

    try:
        handle_contract.is_allowed_to_change_contract(contract_id, request.user)
    except:
        return render(request, "dashboard/page_blocked.html")

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
            "taken_artist_dates": handle_contract.get_artist_taken_dates(
                contract_artist
            ),
            "taken_venues_dates": handle_contract.get_venues_taken_dates(
                contract_artist
            ),
            "taken_contract_artist_date": handle_contract.get_contract_artist_date(
                contract_artist
            )
            # get date of contracs of these customer and artist
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
        handle_contract.add_contract_members_access(contract_artist)
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
    print(artists)
    context = {
        "contracts": artists,
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
        "upcoming_contracts": handle_contract.get_upcoming_events(customer, date),
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
            try:
                contr = form.save()
                contr.customer = customer
                contr.artist = contract.artist
                contr.contract = handle_contract.rerender_contract(contr)
                taken_artist = handle_contract.handle_artist_taken(contr, True)
                if taken_artist:
                    return taken_artist
                taken_venue = handle_contract.handle_venue_taken(contr, True)
                if taken_venue:
                    return taken_venue
                contr.save()
            except Exception as err:
                messages.error(
                    request,
                    "Contract with this customer and artist for this date already exists",
                )
                return HttpResponseRedirect(
                    reverse(
                        "customer_edit_contract", kwargs={"contract_id": contract.id}
                    )
                )

            return HttpResponseRedirect(
                reverse("preview_artist_contract", kwargs={"contract_id": contract.id})
            )

    else:
        form = ContractArtistEditForm(companies, venues, instance=contract)

    context = {
        "form": form,
        "customer": customer,
        "artist": contract.artist,
        "error_message": request.COOKIES.get("error_message"),
        "from_edit": request.COOKIES.get("from_edit"),
        "contract": contract,
    }
    response = render(request, "contract/edit_contract.html", context=context)
    response.delete_cookie("error_message")
    response.delete_cookie("from_edit")
    return response


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


def hide_contract(request, contract_id, date):

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
                "date": date,
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

    try:
        handle_customer.is_allowed_to_change_customer(customer_id, request.user)
    except:
        return render(request, "dashboard/page_blocked.html")

    customer = handle_customer.get_customer_by_id(customer_id)
    contracts = handle_contract.get_hidden_contracts(customer)
    context = {
        "hidden": True,
        "contracts": contracts,
        "customer": customer,
        "today_today": str(datetime.today().date()),
    }

    return render(request, "contract/artists_list.html", context=context)


def get_visible_contracts_for_user(request, user_id):

    # if not user_handle.is_allowed_to_create_contract(user_id):
    #     return render(request, "dashboard/page_blocked.html")

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

    try:
        user_handle.is_allowed_to_create_contract(user_id)
    except:
        return render(request, "dashboard/page_blocked.html")

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
            handle_contract.add_user_to_event_contract_team(
                contract_obj.id, request.user, "admin"
            )
            taken_artist = handle_contract.handle_artist_taken_from_user(contract_obj)
            if taken_artist:
                return taken_artist
            taken_venue = handle_contract.handle_venue_taken_from_user(contract_obj)
            if taken_venue:
                return taken_venue

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
            print(form.errors)
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
            try:
                contr = form.save()
                print(contr)
                contr.customer = customer
                contr.artist = contract.artist
                contr.contract = handle_contract.rerender_contract(contr)
                taken_artist = handle_contract.handle_artist_taken_from_user(
                    contr, True
                )
                if taken_artist:
                    return taken_artist
                taken_venue = handle_contract.handle_venue_taken_from_user(contr, True)
                if taken_venue:
                    return taken_venue
                contr.save()
            except Exception as err:
                messages.error(
                    request,
                    "Contract with this customer and artist for this date already exists",
                )
                return HttpResponseRedirect(
                    reverse("user_edit_contract", kwargs={"contract_id": contract.id})
                )

            return HttpResponseRedirect(
                reverse("preview_artist_contract", kwargs={"contract_id": contract.id})
            )

    else:
        form = ContractArtistEditForm(companies, venues, instance=contract)

    context = {
        "form": form,
        "customer": customer,
        "artist": contract.artist,
        "error_message": request.COOKIES.get("error_message_from_user"),
        "from_edit": request.COOKIES.get("from_edit_user"),
        "contract": contract,
    }
    response = render(request, "contract/user_edit_contract.html", context=context)
    response.delete_cookie("error_message_from_user")
    response.delete_cookie("from_edit_user")
    return response


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
