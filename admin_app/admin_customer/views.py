from admin_app.decorators import user_is_admin
from customer.models import (
    Customer,
    CustomerAccess,
    CustomerContacts,
    CustomerRequestsStorage,
)
from customer.services import handle_customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.list import ListView
from users.models import User
from users.services import user_actions, user_handle

from .forms import (
    CustomerAccessForm,
    CustomerContactsForm,
    CustomerForm,
    CustomerRequestStorageForm,
)


class CustomerListView(LoginRequiredMixin, ListView):

    model = Customer
    template_name = "admin/pages/customer/customer/all.html"
    context_object_name = "customers"


@login_required(login_url="login")
@user_is_admin
def add_new_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer_obj = form.save()

            try:
                handle_customer.add_user_can_change(
                    customer_obj, user_handle.get_user_by_email(request.POST["user"])
                )
            except Exception as ex:
                print(ex)
                messages(request, "something went wrong")

            customer_obj.save()
            return HttpResponseRedirect(reverse("admin_get_all_customers"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerForm()

    users = User.objects.all()
    return render(
        request,
        "admin/pages/customer/customer/add_update.html",
        {"form": form, "users": users},
    )


@login_required(login_url="login")
@user_is_admin
def change_details_customer(request, customer_id):

    customer = handle_customer.get_customer_by_id(customer_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_customers"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "admin/pages/customer/customer/update.html", {"form": form})


@login_required(login_url="login")
@user_is_admin
def delete_customer(request, customer_id):

    try:
        handle_customer.delete_customer(customer_id)
    except Exception as ex:
        print(ex)
    return HttpResponseRedirect(reverse("admin_get_all_customers"))


class CustomerContactsListView(LoginRequiredMixin, ListView):

    model = CustomerContacts
    template_name = "admin/pages/customer/contacts/all.html"
    context_object_name = "contacts"


@login_required(login_url="login")
@user_is_admin
def add_new_customer_contacts(request):
    if request.method == "POST":
        form = CustomerContactsForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_customer_contacts"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerContactsForm()
    return render(
        request, "admin/pages/customer/contacts/add_update.html", {"form": form}
    )


@login_required(login_url="login")
@user_is_admin
def change_details_customer_contacts(request, customer_contacts_id):

    customer_contacts = handle_customer.get_customer_contacts_by_id(
        customer_contacts_id
    )
    if request.method == "POST":
        form = CustomerContactsForm(
            request.POST, request.FILES, instance=customer_contacts
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_customer_contacts"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerContactsForm(instance=customer_contacts)
    return render(
        request, "admin/pages/customer/contacts/add_update.html", {"form": form}
    )


@login_required(login_url="login")
@user_is_admin
def delete_customer_contacts(request, customer_contacts_id):

    try:
        handle_customer.delete_customer_contacts(customer_contacts_id)
    except Exception as ex:
        print(ex)
    return HttpResponseRedirect(reverse("admin_get_all_customer_contacts"))


class CustomerAccesstListView(LoginRequiredMixin, ListView):

    model = CustomerAccess
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/customer/access/all.html"
    context_object_name = "access"


@login_required(login_url="login")
@user_is_admin
def add_new_customer_access(request):
    if request.method == "POST":
        form = CustomerAccessForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_customer_access"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerAccessForm()
    return render(
        request, "admin/pages/customer/access/add_update.html", {"form": form}
    )


@login_required(login_url="login")
@user_is_admin
def change_details_customer_access(request, access_id):

    customer_access = handle_customer.get_customer_access_by_id(access_id)
    if request.method == "POST":
        form = CustomerAccessForm(request.POST, instance=customer_access)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_customer_access"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerAccessForm(instance=customer_access)
    return render(
        request, "admin/pages/customer/access/add_update.html", {"form": form}
    )


@login_required(login_url="login")
@user_is_admin
def admin_delete_customer_access(request, access_id):
    print("here")
    try:
        handle_customer.delete_customer_access(access_id)
    except Exception as ex:
        print(ex)
    return HttpResponseRedirect(reverse("admin_get_all_customer_access"))


class CustomerRequestStorageListView(LoginRequiredMixin, ListView):

    model = CustomerRequestsStorage
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/customer/request_storage/all.html"
    context_object_name = "requests"


@login_required(login_url="login")
@user_is_admin
def add_new_customer_request_storage(request):
    if request.method == "POST":
        form = CustomerRequestStorageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_customer_requests"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerRequestStorageForm()
    return render(
        request, "admin/pages/customer/request_storage/add_update.html", {"form": form}
    )


@login_required(login_url="login")
@user_is_admin
def change_details_customer_request_storage(request, request_storage_id):

    customer_request_storage = handle_customer.get_customer_request_storage_by_id(
        request_storage_id
    )
    if request.method == "POST":
        form = CustomerRequestStorageForm(
            request.POST, request.FILES, instance=customer_request_storage
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_customer_requests"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CustomerRequestStorageForm(instance=customer_request_storage)

    context = {
        "form": form,
    }
    return render(
        request, "admin/pages/customer/request_storage/add_update.html", context
    )


@login_required(login_url="login")
@user_is_admin
def admin_delete_customer_request_storage(request, request_storage_id):
    try:
        handle_customer.delete_customer_request_storage(request_storage_id)
    except Exception as ex:
        print(ex)
    return HttpResponseRedirect(reverse("admin_get_all_customer_requests"))
