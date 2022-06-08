from cgitb import handler
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
    EventForm,
    EventProductForm,
    TimeClockForm,
)
from .models import EventTeam
from .services import handle_event, constants
from contract.services import handle_contract


class MyEventsListView(LoginRequiredMixin, ListView):

    model = EventTeam
    template_name = "event/my_events_list.html"
    context_object_name = "event_team"

    def get_queryset(self):
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
        last_time_clock = handle_event.get_event_time_clock(event).last()
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
        form = EventProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                name = form.cleaned_data["name"]
                picture = form.cleaned_data["picture"]
                price = form.cleaned_data["price"]
                count = form.cleaned_data["count"]
                rental_product = handle_event.create_rental_product(name, picture)
                handle_event.add_event_rental_product(
                    event_id, rental_product, price, count
                )
            except Exception as er:
                print(er)
                messages.error(request, "Something went wrong")
        else:
            messages.error(request, "Form is invalid")

    return HttpResponseRedirect(
        reverse("get_event_details", kwargs={"event_id": event_id, "time_clock_id": -1})
    )


@login_required(login_url="login")
def get_event_products_list(request, event_id):
    event_products = handle_event.get_event_products(event_id)
    contract = handle_contract.get_contract_artist_by_id(event_id)
    print(contract)
    return render(
        request,
        "event/event_products_list.html",
        {"products": event_products, "event": contract},
    )


@login_required(login_url="login")
def delete_event_product(request, event_id, product_id):

    try:
        handle_event.delete_event_product(product_id)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse("get_event_products_list", kwargs={"event_id": event_id})
    )


@login_required(login_url="login")
def edit_event_product(request, event_id, product_id):

    product = handle_event.get_event_product_by_id(product_id)
    if request.method == "POST":
        try:
            if not handle_event.validate_product(request.POST):
                messages.error(request, "Form is invalid")
                return HttpResponseRedirect(
                    reverse(
                        "edit_event_product",
                        kwargs={"event_id": event_id, "product_id": product_id},
                    )
                )
            name = request.POST["name"]
            picture = request.FILES.get("picture")
            price = request.POST["price"]
            count = request.POST["count"]

            rental_product = handle_event.update_rental_product(name, picture, product)
            handle_event.update_event_rental_product(
                product, rental_product, price, count
            )
        except Exception as er:
            raise (er)
            messages.error(request, "Something went wrong")

        return HttpResponseRedirect(
            reverse("get_event_products_list", kwargs={"event_id": event_id})
        )

    context = {"product": product}

    return render(request, "event/edit_event_product.html", context=context)
