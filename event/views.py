from cgitb import handler
from datetime import date, datetime
import time
from artist.decorators import user_has_perm_to_change
from company.models import Company
from customer.services import handle_customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.list import ListView
from users.services import user_handle
from venue.services import handle_venue
from .forms import (
    ArtistEventTeamForm,
    CompanyContractProduct,
    CompanyContractProductEdit,
    ConfirmEventProductForm,
    EventForm,
    EventProductForm,
    TimeClockForm,
)
from .models import EventTeam
from .services import handle_event, constants
from contract.services import handle_contract
from artist.services import user_artists, constants as artist_constants


class MyEventsListView(LoginRequiredMixin, ListView):

    model = EventTeam
    template_name = "event/my_events_list.html"
    context_object_name = "event_team"

    def get_queryset(self, *args, **kwargs):
        return handle_event.get_event_contracts_for_user(self.request.user)

    def dispatch(self, *args, **kwargs):
        dispatch_method = super(MyEventsListView, self).dispatch

        if not (
            self.request.user.is_staff
            or EventTeam.objects.filter(user=self.request.user)
        ):
            raise PermissionDenied

        return dispatch_method(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_perm"] = self.request.user.is_staff
        return context


@login_required(login_url="login")
def get_my_events(request, date):

    if date == "0":
        event_date = str(datetime.today().date())
    else:
        event_date = date
    context = {
        "event_team": handle_event.get_event_contracts_for_user(
            request.user, event_date
        ),
        "has_perm": request.user.is_staff,
        "today_date": event_date,
        "today_today": str(datetime.today().date()),
        "week_days_list": user_artists.get_week_days_list(
            datetime.strptime(event_date, "%Y-%m-%d").date(),
            artist_constants.week_names_count[
                datetime.strptime(event_date, "%Y-%m-%d").date().strftime("%A")
            ],
        ),
        "upcoming_contracts": handle_event.get_upcoming_events(
            request.user, event_date
        ),
    }
    return render(request, "event/my_events_list.html", context)


# @login_required(login_url="login")
# @user_has_perm_to_change
# def add_new_event(request):
#     venue_queryset = handle_event.get_venue_queryset(request.user)

#     if request.method == "POST":
#         form = EventForm(venue_queryset, request.POST)
#         print(request.POST)
#         if form.is_valid():
#             event_obj = form.save()
#             try:
#                 event_obj.save()
#                 handle_event.add_user_to_event_team(
#                     event_obj.id, request.user, "creator"
#                 )
#             except Exception as er:
#                 messages.error(request, er)
#             return HttpResponseRedirect(
#                 reverse("get_event_details", kwargs={"event_id": event_obj.id})
#             )
#         else:
#             messages.error(request, "Opps, there are some problems")

#     else:
#         form = EventForm(
#             venue_queryset=venue_queryset,
#         )
#     return render(request, "event/add_new_event.html", {"form": form})


@login_required(login_url="login")
def get_event_details(request, event_id, time_clock_id):

    try:
        handle_event.is_allowed_to_change(event_id, request.user)
    except Exception as err:
        return render(request, "dashboard/page_blocked.html")

    try:
        event = handle_contract.get_contract_artist_by_id(event_id)
    except:
        event = None

    form_edit_time_clock = (
        TimeClockForm(instance=handle_event.get_time_clock(time_clock_id))
        if int(time_clock_id) > 0
        else 0
    )

    # form event_user_team
    artist_team_users = handle_event.artist_user_team(event.artist)
    form_event_user_team = ArtistEventTeamForm(artist_team_users, request.POST)
    # --------------------

    if handle_event.get_event_time_clock(event):
        last_time_clock = handle_event.get_event_time_clock(event).last().id
    else:
        last_time_clock = -1

    context = {
        "event": event,
        "is_allowed_to_change": handle_event.is_allowed_to_change(
            event_id, request.user
        ),
        "users_in_team": handle_event.get_users_team(event_id, request.user),
        # "form": form,
        "my_artists": handle_event.get_my_artists(request.user),
        "aval_users": handle_event.get_avaluable_users(event),
        "form_event": EventProductForm(),
        "existing_time_clock": handle_event.get_event_time_clock(event),
        "last_time_clock_id": last_time_clock,
        "time_clock_id": int(time_clock_id),
        "form": TimeClockForm(),
        "form_edit_time_clock": form_edit_time_clock,
        "form_event_user_team": form_event_user_team,
        "artist_team_users": handle_event.artist_user_team_queryset(event.artist),
        "chosen_event_artist_users": handle_event.get_all_event_artist_team(event),
        "tod_date": date.today(),
    }

    return render(request, "event/event_details.html", context=context)


@login_required(login_url="login")
def add_time_clock_to_event(request, event_id, last_clock_time_id):

    if request.method == "POST":
        form = TimeClockForm(request.POST)
        if form.is_valid():
            time_clock = form.save(commit=False)
            if (
                int(last_clock_time_id) > 0
                and form.cleaned_data["start_time"]
                < handle_event.get_time_clock(last_clock_time_id).end_time
            ):
                messages.error(request, "start time is lover than previous element")
            else:
                time_clock.save()
                contract_time_clock = handle_event.get_or_create_contract_clock(
                    event_id
                )[0]
                handle_event.add_clock_to_event_clock(contract_time_clock, time_clock)

            return HttpResponseRedirect(
                reverse(
                    "get_event_details",
                    kwargs={"event_id": event_id, "time_clock_id": -1},
                )
            )


@login_required(login_url="login")
def remove_time_clock_to_event(request, event_id, time_clock_id):

    contract_time_clock = handle_event.get_or_create_contract_clock(event_id)[0]
    handle_event.remove_clock_to_event_clock(contract_time_clock, time_clock_id)

    return HttpResponseRedirect(
        reverse("get_event_details", kwargs={"event_id": event_id, "time_clock_id": -1})
    )


@login_required(login_url="login")
def edit_time_clock_to_event(request, event_id, time_clock_id):

    if request.method == "POST":
        form = TimeClockForm(
            request.POST, instance=handle_event.get_time_clock(time_clock_id)
        )
        if form.is_valid():
            elem = form.save(commit=False)
            if handle_event.is_time_fittable(
                event_id,
                form.cleaned_data["start_time"],
                form.cleaned_data["end_time"],
                time_clock_id,
            ):
                messages.error(request, "This time is not suttable for this time clock")
            else:
                elem.save()

            return HttpResponseRedirect(
                reverse(
                    "get_event_details",
                    kwargs={"event_id": event_id, "time_clock_id": -1},
                )
            )
        else:
            print(form.errors)


@login_required(login_url="login")
def add_event_artist_team(request, event_id):
    contract = handle_contract.get_contract_artist_by_id(event_id)
    artist_team_users = handle_event.artist_user_team(contract.artist)

    if request.method == "POST":
        form = ArtistEventTeamForm(artist_team_users, request.POST)
        if form.is_valid():
            handle_event.add_event_artist_team(
                contract, form.cleaned_data["artist_team"]
            )
            return HttpResponseRedirect(
                reverse(
                    "get_event_details",
                    kwargs={"event_id": event_id, "time_clock_id": -1},
                )
            )
        else:
            messages.error(request, "Opps, there are some problems")


@login_required(login_url="login")
def edit_event_artist_team(request, event_id, artist_users_team):
    contract = handle_contract.get_contract_artist_by_id(event_id)

    handle_event.edit_event_artist_team(contract, artist_users_team)
    return HttpResponseRedirect(
        reverse(
            "get_event_details",
            kwargs={"event_id": event_id, "time_clock_id": -1},
        )
    )


# @login_required(login_url="login")
# @user_has_perm_to_change
# def update_event(request, event_id):
#     venue_queryset = handle_event.get_venue_queryset(request.user)
#     event = handle_event.get_event_by_id(event_id)

#     if request.method == "POST":
#         form = EventForm(
#             venue_queryset,
#             request.POST,
#             instance=event,
#         )
#         if form.is_valid():
#             event_obj = form.save()

#             try:
#                 event_obj.save()
#             except Exception as er:
#                 messages.error(request, er)
#             return HttpResponseRedirect(
#                 reverse("get_event_details", kwargs={"event_id": event_obj.id})
#             )
#         else:
#             messages.error(request, "Opps, there are some problems")
#     else:
#         form = EventForm(
#             venue_queryset=venue_queryset,
#             instance=event,
#         )
#     return render(request, "event/update_event.html", {"form": form})


# @login_required(login_url="login")
# def delete_event(request, event_id):

#     if not handle_event.is_allowed_to_change(event_id, request.user):
#         raise PermissionDenied
#     try:
#         handle_event.delete_event(event_id)
#     except Exception as ex:
#         print(ex)
#     return HttpResponseRedirect(reverse("get_all_events"))


# @login_required(login_url="login")
# def delete_artist_from_event(request, event_id, artist_id):

#     if not handle_event.is_allowed_to_change(event_id, request.user):
#         raise PermissionDenied
#     try:
#         handle_event.delete_artist_from_event(event_id, artist_id)
#         event = handle_event.get_event_by_id(event_id)
#         event.save()
#     except Exception as ex:
#         print(ex)
#     return HttpResponseRedirect(
#         reverse("get_event_artist_list", kwargs={"event_id": event_id})
#     )


# @login_required(login_url="login")
# def load_contract_for_event(request, event_id):

#     event = handle_event.get_event_by_id(event_id)
#     event_contract = event.contract

#     return render(
#         request,
#         "event/contract_view.html",
#         {"contract": event_contract, "event": event},
#     )


# @login_required(login_url="login")
# def get_event_artist_list(request, event_id):
#     event_artists = handle_event.get_event_artists(event_id)
#     event = handle_event.get_event_by_id(event_id)
#     return render(
#         request,
#         "event/event_artists_list.html",
#         {"artists": event_artists, "event": event},
#     )


@login_required(login_url="login")
def add_user_to_team(request, event_id):

    if request.method == "POST":
        try:
            contract = handle_contract.get_contract_artist_by_id(event_id)
            user = user_handle.get_user_by_email(request.POST.get("users_for_adding"))
            handle_venue.add_user_can_change(contract.venue, user, False)
            handle_event.add_user_to_team(
                event_id,
                request.POST.get("users_for_adding"),
                request.POST.get("users_for_adding_role"),
            )
        except Exception as er:
            raise er
            messages.error(request, er)

    return HttpResponseRedirect(
        reverse("get_event_details", kwargs={"event_id": event_id, "time_clock_id": -1})
    )


@login_required(login_url="login")
def edit_user_in_team(request, event_id, user_email, role):

    try:
        handle_event.update_user_in_team(event_id, user_email, role)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse("get_event_details", kwargs={"event_id": event_id, "time_clock_id": -1})
    )


@login_required(login_url="login")
def delete_user_from_team(request, event_id, user_email):

    try:
        handle_event.delete_user_from_team(event_id, user_email)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse("get_event_details", kwargs={"event_id": event_id, "time_clock_id": -1})
    )


@login_required(login_url="login")
def add_event_product(request, event_id):

    if request.method == "POST":
        form = CompanyContractProduct([], request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.errors)

    return HttpResponseRedirect(
        reverse("get_event_products_list", kwargs={"event_id": event_id})
    )


@login_required(login_url="login")
def get_event_products_list(request, event_id, product_id):
    event_products = handle_event.get_event_products(event_id)
    contract = handle_contract.get_contract_artist_by_id(event_id)
    errors = ""
    if request.method == "POST":
        form = CompanyContractProduct(
            handle_event.get_company_products(contract), request.POST
        )
        if form.is_valid():
            con_com_prod = form.save(commit=False)  # contract company product
            avaluable_product_count = handle_event.get_product_aval_count(
                con_com_prod.product, contract
            )
            if con_com_prod.product.in_stock < con_com_prod.count:
                errors = (
                    "Unfortunatelly for this date this count of product is unavaluable"
                )
            else:
                con_com_prod.save()
                contract_product_obj = handle_contract.get_or_create_c_c_prod(contract)[
                    0
                ]
                contract_product_obj.confirmed = False
                product_for_cont_exists = (
                    handle_event.check_prod_exists_in_contr_products(
                        contract, con_com_prod.product
                    )
                )
                if product_for_cont_exists:
                    product_for_cont_exists.count += con_com_prod.count
                    product_for_cont_exists.total_price = (
                        product_for_cont_exists.count * con_com_prod.product.price
                    )
                    con_com_prod.product.in_stock -= con_com_prod.count
                    product_for_cont_exists.save()
                else:
                    con_com_prod.total_price = (
                        con_com_prod.count * con_com_prod.product.price
                    )
                    contract_product_obj.products.add(con_com_prod)
                    con_com_prod.product.in_stock -= con_com_prod.count
                con_com_prod.product.save()
                con_com_prod.save()
                contract_product_obj.total_price += (
                    con_com_prod.count * con_com_prod.product.price
                )
                contract_product_obj.count += con_com_prod.count
                contract_product_obj.save()
        else:
            print(form.errors)
            errors = "Unfortunatelly this count of product is out of stock"

    com_products = []

    try:
        com_products = handle_event.get_company_products(contract)
    except Exception as err:
        print(err)
        messages.error(request, "Something went wrong")
    form = CompanyContractProduct(com_products)
    form_edit_c_c_product = (
        CompanyContractProduct(
            com_products,
            instance=handle_event.get_c_product_one(product_id),
        )
        if int(product_id) > 0
        else 0
    )
    cookies_errors = request.COOKIES.get("product_form_error")
    print(event_products)
    response = render(
        request,
        "event/event_products_list.html",
        {
            "products": event_products,
            "total_total_sum": handle_contract.get_or_create_c_c_prod(contract)[
                0
            ].total_price,
            "total_count_sum": handle_contract.get_or_create_c_c_prod(contract)[
                0
            ].count,
            "event": contract,
            "event_products_obj": handle_contract.get_or_create_c_c_prod(contract)[0],
            "form": form,
            "errors": errors or cookies_errors,
            "form_edit": form_edit_c_c_product,
            "product_id": int(product_id),
            "tod_date": date.today(),
        },
    )
    print(date.today(), "heheh")
    response.delete_cookie("product_form_error")
    return response


@login_required(login_url="login")
def delete_event_product(request, event_id, product_id):

    try:
        handle_event.delete_event_product(product_id, event_id)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_event_products_list", kwargs={"event_id": event_id, "product_id": -1}
        )
    )


@login_required(login_url="login")
def edit_event_product(request, event_id, product_id):
    contract = handle_contract.get_contract_artist_by_id(event_id)
    c_product = handle_event.get_c_c_product(product_id)
    c_product_count = c_product.count
    errors = ""
    if request.method == "POST":
        form = CompanyContractProduct([], request.POST, instance=c_product)
        if form.is_valid():
            con_com_prod = form.save(commit=False)  # contract company product
            contract_product_obj = handle_contract.get_or_create_c_c_prod(contract)[0]
            contract_product_obj.confirmed = False
            if con_com_prod.product.in_stock < con_com_prod.count:
                errors = (
                    "Unfortunatelly for this date this count of product is unavaluable"
                )
            else:
                con_com_prod.total_price = (
                    con_com_prod.count * con_com_prod.product.price
                )
                con_com_prod.save()
                count_difference = form.cleaned_data["count"] - c_product_count
                con_com_prod.product.in_stock -= count_difference
                contract_product_obj.count += count_difference
                contract_product_obj.total_price += (
                    count_difference * con_com_prod.product.price
                )
                con_com_prod.product.save()
                contract_product_obj.save()

        else:
            print(form.errors, form.is_bound)
            errors = "Unfortunatelly this count of product is out of stock"

        response = HttpResponseRedirect(
            reverse(
                "get_event_products_list",
                kwargs={"event_id": event_id, "product_id": -1},
            )
        )
        response.set_cookie("product_form_error", errors)
        return response


@login_required(login_url="login")
def load_product_confirmation_page(request, event_id):

    event = handle_contract.get_contract_artist_by_id(event_id)

    if request.method == "POST":
        form = ConfirmEventProductForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(
                reverse(
                    "confirm_event_product_from_customer",
                    kwargs={"event_id": event_id},
                )
            )
    form = ConfirmEventProductForm()

    context = {"company": event.company, "event": event, "form": form}

    return render(request, "event/customer_confirm_event_product.html", context)


@login_required(login_url="login")
def confirm_event_product_from_customer(request, event_id):
    print("here")

    try:
        handle_event.confirm_product(event_id)
    except Exception as ex:
        print(ex)
        messages.error(request, ex)

    return HttpResponseRedirect(
        reverse(
            "get_event_products_list", kwargs={"event_id": event_id, "product_id": -1}
        )
    )
