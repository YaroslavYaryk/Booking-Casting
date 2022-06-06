from datetime import datetime
from artist.decorators import user_has_perm_to_change
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.list import ListView
from users.services import user_handle

from .forms import VenueAddForm, VenueContactsAddForm
from .models import Venue, VenueAccess, VenueContacts, VenuePictures
from .services import handle_request_storage, handle_venue, handle_venue_contacts
from artist.services import user_artists, constants as artist_constants
from customer.services import handle_customer
from contract.services import handle_contract


class MyVenueListView(LoginRequiredMixin, ListView):

    model = VenueAccess
    template_name = "venue/my_venue_list.html"
    context_object_name = "venue_access"

    def get_queryset(self):
        return handle_venue.get_customers_for_user(self.request.user)

    def dispatch(self, *args, **kwargs):
        dispatch_method = super(MyVenueListView, self).dispatch
        if not (
            self.request.user.is_staff
            or VenueAccess.objects.filter(access=self.request.user)
        ):
            raise PermissionDenied

        return dispatch_method(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_perm"] = self.request.user.is_staff
        return context


@login_required(login_url="login")
@user_has_perm_to_change
def add_new_venue(request):
    if request.method == "POST":
        form = VenueAddForm(request.POST)

        if form.is_valid():
            venue_obj = form.save()
            try:
                handle_venue.add_user_can_change(venue_obj, request.user)
            except Exception as ex:
                print(ex)
            venue_obj.save()

            return HttpResponseRedirect(
                reverse(
                    "get_venue_details",
                    kwargs={
                        "venue_id": venue_obj.id,
                    },
                )
            )
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = VenueAddForm()
    return render(request, "venue/add_venue.html", {"form": form})


# # HANDLE When user hasnt permission to change - he cant change or see form of user contacts
# # check if user contacts for thois customer is filled, otherway dont even display contact info


@login_required(login_url="login")
def get_venue_details(request, venue_id):

    try:
        handle_venue.is_allowed_to_change(venue_id, request.user)
    except:
        return render(request, "dashboard/page_blocked.html")

    venue_contacts = handle_venue_contacts.get_or_create_customer_by_id(venue_id)
    users_except_admin = [("", "")] + handle_customer.get_users_except_admin()
    if request.method == "POST":

        if not handle_venue.is_allowed_to_change(venue_id, request.user):
            raise PermissionDenied

        form = VenueContactsAddForm(venue_contacts, users_except_admin, request.POST)
        if form.is_valid():
            try:
                handle_venue.add_venue_contacts(venue_contacts, form.cleaned_data)
            except Exception as err:
                print(err)
                raise (err)
                messages.error(request, "Something went wrong")
        else:
            print("nvalid")
    else:
        form = VenueContactsAddForm(venue_contacts, users_except_admin)
    try:
        venue = handle_venue.get_venue_by_id(venue_id)
    except:
        venue = None
    context = {
        "venue": venue,
        "is_allowed_to_change": handle_venue.is_allowed_to_change(
            venue_id, request.user
        ),
        "users_have_access": handle_venue.get_users_can_change(venue_id, request.user),
        "form": form,
        "contacts_exists": handle_venue_contacts.contacts_exists(venue_contacts),
        "venue_contacts": venue_contacts,
        "aval_users": handle_venue.get_avaluable_users(venue),
        "images": handle_venue.get_venue_pictures(venue_id),
        "image_preview": handle_venue.get_venue_pictures(venue_id).first(),
        "my_contracts": handle_venue.get_all_my_contracts(venue),
        "us": user_handle.get_user_by_email(venue_contacts.epost),
        "today_today": str(datetime.today().date()),
    }

    return render(request, "venue/venue_details.html", context=context)


@login_required(login_url="login")
def change_details_venue(request, venue_id):

    if not handle_venue.is_allowed_to_change(venue_id, request.user):
        raise PermissionDenied

    venue = handle_venue.get_venue_by_id(venue_id)
    if request.method == "POST":
        form = VenueAddForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    "get_venue_details",
                    kwargs={
                        "venue_id": venue.id,
                    },
                )
            )
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = VenueAddForm(instance=venue)
    return render(request, "venue/change_venue.html", {"form": form})


@login_required(login_url="login")
def send_request_to_change_venue(request, venue_id):
    user = request.user
    try:
        handle_request_storage.send_request(user, venue_id)
    except Exception as ex:

        messages.error(request, ex)

    return HttpResponseRedirect(reverse("get_all_messages"))


# @login_required(login_url='login')
# def handle_change_request(request, r_from, r_to, customer_id):

#     if request.method == 'POST':
#         granted = list(request.POST.keys())[-1] == "accept"
#         try:
#             request_user_to_change.handle_request_form(r_from, r_to, customer_id,  granted )
#         except Exception as ex:
#             print(ex)
#             messages.success(request, 'Something went wrong')
#         return HttpResponseRedirect(reverse("home"))

#     else:
#         print("get")

#     context = {
#         "requester": user_handle.get_user_by_id(r_from),
#         "owner" : user_handle.get_user_by_id(r_to),
#         "customer" : handle_customer.get_customer_by_id(customer_id),
#         "is_choice" : False,
#         "body" : "customer"
#     }

#     return render(request, "dashboard/handle_request.html", context=context)


@login_required(login_url="login")
def delete_venue(request, venue_id):

    if not handle_venue.is_allowed_to_change(venue_id, request.user):
        raise PermissionDenied
    try:
        handle_venue.delete_venue(venue_id)
    except Exception as ex:
        print(ex)

    if not (request.user.is_staff or VenueAccess.objects.filter(access=request.user)):
        return HttpResponseRedirect(reverse("home"))

    return HttpResponseRedirect(reverse("my_customers"))


def delete_user_from_venue_changeble(request, venue_id, user_id):

    try:
        handle_venue.delete_from_changeble(venue_id, user_id)
    except Exception as ex:
        print(ex)

    return HttpResponseRedirect(
        reverse(
            "get_venue_details",
            kwargs={"venue_id": venue_id},
        )
    )


@login_required(login_url="login")
def add_user_permission_to_change_or_see_venue(
    request, venue_id, user_phone, perm_type
):

    try:
        handle_venue.add_permission_to_change(venue_id, user_phone, perm_type)
    except Exception as er:
        print(er)
        messages.error(request, er)

    return HttpResponseRedirect(
        reverse(
            "get_venue_details",
            kwargs={
                "venue_id": venue_id,
            },
        )
    )


@login_required(login_url="login")
def change_user_permission_to_change_or_see_venue(request, access_id, perm_type):
    venue = ""
    try:
        venue = handle_venue.change_permission_to_change(
            access_id, perm_type, request.user
        )
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_venue_details",
            kwargs={
                "venue_id": venue.id,
            },
        )
    )


@login_required(login_url="login")
def upload_picture_handle(request, venue_id):

    if not handle_venue.is_allowed_to_change(venue_id, request.user):
        raise PermissionDenied

    if request.method == "POST":
        images = request.FILES.getlist("images")
        for image in images:

            if not (
                image.name.endswith(".jpg")
                or image.name.endswith(".jpeg")
                or image.name.endswith(".png")
            ):
                messages.error(request, "This file type is not supported!")
                return HttpResponseRedirect(
                    reverse(
                        "get_venue_details",
                        kwargs={
                            "venue_id": venue_id,
                        },
                    )
                )
            else:
                VenuePictures.objects.create(
                    venue=handle_venue.get_venue_by_id(venue_id), file=image
                )

    return HttpResponseRedirect(
        reverse(
            "get_venue_details",
            kwargs={
                "venue_id": venue_id,
            },
        )
    )


@login_required(login_url="login")
def delete_venue_picture(request, venue_id, picture_id):
    try:
        handle_venue.delete_venue_picture(picture_id)
    except Exception as er:
        print(er)
        messages.error(request, er)

    return HttpResponseRedirect(
        reverse(
            "get_venue_details",
            kwargs={
                "venue_id": venue_id,
            },
        )
    )


@login_required(login_url="login")
def get_all_venue_events(request, venue_id):

    my_events = handle_venue.get_my_events(venue_id)
    context = {"events": my_events}

    return render(request, "venue/venue_events.html", context=context)


@login_required(login_url="login")
def invite_user(request, venue_id, user_email):

    if user_handle.filter_user_email(user_email):
        messages.error(request, "This user already exists")
        return HttpResponseRedirect(
            reverse(
                "get_venue_details",
                kwargs={
                    "venue_id": venue_id,
                },
            )
        )

    try:
        user_artists.send_invitation_message(
            request.user,
            user_email,
            "dashboard/invitation.html",
            "http://127.0.0.1:8000/",
        )
    except Exception as er:
        print(er)
        messages.error(request, "Opps, there are some problems")

    messages.success(request, "Successfully sent invitation link")

    return HttpResponseRedirect(
        reverse(
            "get_venue_details",
            kwargs={
                "venue_id": venue_id,
            },
        )
    )


@login_required(login_url="login")
def get_venue_contracts(request, venue_id, date):

    venue = handle_venue.get_venue_by_id(venue_id)
    try:
        venue_contracts = handle_venue.get_my_contracts(venue, date)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    context = {
        "venue": venue,
        "contracts": venue_contracts,
        "today_date": date,
        "today_today": str(datetime.today().date()),
        "week_days_list": user_artists.get_week_days_list(
            datetime.strptime(date, "%Y-%m-%d").date(),
            artist_constants.week_names_count[
                datetime.strptime(date, "%Y-%m-%d").date().strftime("%A")
            ],
        ),
        "visible": True,
        "upcoming_contracts": handle_venue.get_upcoming_contracts(venue, date),
    }

    return render(request, "venue/venue_contracts.html", context)


@login_required(login_url="login")
def get_venue_hidden_contracts(request, venue_id):

    venue = handle_venue.get_venue_by_id(venue_id)
    try:
        venue_contracts = handle_venue.get_my_hidden_contracts(venue)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    context = {
        "venue": venue,
        "contracts": venue_contracts,
        "today_today": str(datetime.today().date()),
        "visible": False,
    }

    return render(request, "venue/venue_contracts.html", context)


@login_required(login_url="login")
def hide_artist_contract(request, contract_id, date):

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.hide_contract(contract)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_venue_contracts",
            kwargs={"venue_id": contract.venue.id, "date": date},
        )
    )


@login_required(login_url="login")
def unhide_artist_contract(request, contract_id):

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.unhide_contract(contract)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_hidden_contracts_venue",
            kwargs={"venue_id": contract.venue.id},
        )
    )
