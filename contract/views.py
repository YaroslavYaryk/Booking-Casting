from django.shortcuts import render
from customer.services import handle_customer
from .forms import ContractArtistForm, ContractForm, ContractArtistEditForm
from venue.services import handle_venue
from event.services import handle_event
from django.contrib import messages
from django.urls.base import reverse
from django.http import HttpResponseRedirect
from .services import handle_contract


def create_contract(request, customer_id):

    customer = handle_customer.get_customer_by_id(customer_id)
    aval_arists = handle_customer.get_avaluable_artists(customer)
    companies = handle_event.get_company_queryset(request.user)
    venues = handle_event.get_venue_queryset(request.user)

    if request.method == "POST":
        form = ContractArtistForm(aval_arists, companies, venues, request.POST)

        if form.is_valid():
            contract_obj = form.save(commit=False)
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
            messages.error(request, "Something went wrong")

    else:
        form = ContractArtistForm(aval_arists, companies, venues)

    context = {"form": form, "customer": customer}
    return render(request, "contract/make_contract.html", context=context)


def get_contract(request, contract_id):

    rendered_template = handle_contract.get_rendered_contract(request, contract_id)
    cotract_artist = handle_contract.get_contract_artist_by_id(contract_id)
    # return rendered_template
    if request.method == "POST":
        form = ContractForm(rendered_template, request.POST)
        if form.is_valid():
            print(form.cleaned_data["contract"])
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

    return render(
        request, "contract/preview_contract.html", {"artist": contract_artist}
    )


def save_artist_contract_data(
    request, event_artist_id, date, honorar, payment_methods, comment
):
    contract_artist = handle_contract.get_contract_artist_by_id(event_artist_id)
    contract_artist.date = date
    contract_artist.price = honorar
    contract_artist.payment_methods = payment_methods
    contract_artist.comment = comment
    contract_artist.save()

    try:
        handle_contract.create_pdf_contract(contract_artist)
    except Exception as err:
        print(err)
        messages.error(request, "something went wrong")

    return HttpResponseRedirect(
        reverse(
            "customer_details",
            kwargs={
                "customer_id": contract_artist.customer.id,
            },
        )
    )


def get_all_contracted_artists(request, customer_id):

    customer = handle_customer.get_customer_by_id(customer_id)
    artists = handle_contract.get_contracted_artists(customer)
    context = {"artists": artists, "customer": customer}

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

    if request.method == "POST":
        form = ContractArtistEditForm(request.POST, instance=contract)

        if form.is_valid():
            contr = form.save()
            contr.customer = customer
            contr.contract = handle_contract.rerender_contract(contr)
            contr.save()
            return HttpResponseRedirect(
                reverse("preview_artist_contract", kwargs={"contract_id": contract.id})
            )
        else:
            messages.error(request, "Something went wrong")
    else:
        form = ContractArtistEditForm(instance=contract)

    context = {"form": form, "customer": customer, "artist": contract.artist}
    return render(request, "contract/edit_contract.html", context=context)


def get_contract_view(request, contract_id):

    rendered_template = handle_contract.get_rendered_contract(request, contract_id)
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
