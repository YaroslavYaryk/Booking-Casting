from admin_app.decorators import user_is_admin
from customer.models import *
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
from users.services import user_handle
from venue.models import (Venue, VenueAccess, VenueContacts, VenuePictures,
                          VenueRequestsStorage)
from venue.services import (handle_request_storage, handle_venue,
                            handle_venue_access, handle_venue_picture)

from .forms import (VenueAccessForm, VenueContactsAddForm, VenueForm,
                    VenuePictureForm, VenueRequestStorageForm)


class VenueListView(LoginRequiredMixin, ListView):

    model = Venue
    template_name = "admin/pages/venue/venue/all.html"
    context_object_name = 'venues'


@login_required(login_url='login')
@user_is_admin
def add_new_venue(request):
    if request.method == 'POST':
        form = VenueForm( request.POST)

        if form.is_valid():
            venue_obj = form.save()
            try:
                handle_venue.add_user_can_change(venue_obj, user_handle.get_user_by_email(request.POST["user"]))
            except Exception as ex:
                print(ex)
            return HttpResponseRedirect(reverse("admin_get_all_venues"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueForm()
        
    users = User.objects.all()
    return render(request, 'admin/pages/venue/venue/add_update.html', {'form': form, "users": users})



@login_required(login_url='login')
@user_is_admin
def change_details_venue(request, venue_id):
    
    venue = handle_venue.get_venue_by_id(venue_id)
    if request.method == 'POST':
        form = VenueForm( request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venues"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'admin/pages/venue/venue/update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def delete_venue(request, venue_id):

    try:
        handle_venue.delete_venue(venue_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_venues")) 



class VenueContactsListView(LoginRequiredMixin, ListView):
    
    model = VenueContacts
    template_name = "admin/pages/venue/contacts/all.html"
    context_object_name = 'contacts'


@login_required(login_url='login')
@user_is_admin
def add_new_venue_contacts(request):
    if request.method == 'POST':
        form = VenueContactsAddForm( request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_contacts"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueContactsAddForm()
    return render(request, 'admin/pages/venue/contacts/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_venue_contacts(request, venue_contacts_id):
    
    venue_contacts = handle_venue.get_venue_contacts_by_id(venue_contacts_id)
    if request.method == 'POST':
        form = VenueContactsAddForm( request.POST, request.FILES, instance=venue_contacts)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_contacts"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueContactsAddForm(instance=venue_contacts)
    return render(request, 'admin/pages/venue/contacts/add_update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def delete_venue_contacts(request, venue_contacts_id):

    try:
        handle_venue.delete_venue_contacts(venue_contacts_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_venue_contacts")) 


class VenueAccesstListView(LoginRequiredMixin, ListView):
    
    model = VenueAccess
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/venue/access/all.html"
    context_object_name = 'access'



@login_required(login_url='login')
@user_is_admin
def add_new_venue_access(request):
    if request.method == 'POST':
        form = VenueAccessForm( request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_access"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueAccessForm()
    return render(request, 'admin/pages/venue/access/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_venue_access(request, access_id):
    
    venue_access = handle_venue_access.get_venue_access_by_id(access_id)
    if request.method == 'POST':
        form = VenueAccessForm( request.POST, instance=venue_access)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_access"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueAccessForm(instance=venue_access)
    return render(request, 'admin/pages/venue/access/add_update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def admin_delete_venue_access(request, access_id):
    print("here")
    try:
        handle_venue_access.delete_venue_access(access_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_venue_access")) 


class VenueRequestStorageListView(LoginRequiredMixin, ListView):
    
    model = VenueRequestsStorage
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/venue/request_storage/all.html"
    context_object_name = 'requests'



@login_required(login_url='login')
@user_is_admin
def add_new_venue_request_storage(request):
    if request.method == 'POST':
        form = VenueRequestStorageForm( request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_requests"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueRequestStorageForm()
    return render(request, 'admin/pages/venue/request_storage/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_venue_request_storage(request, request_storage_id):
    
    venue_request_storage = handle_request_storage.get_venue_request_storage_by_id(request_storage_id)
    if request.method == 'POST':
        form = VenueRequestStorageForm( request.POST, request.FILES, instance=venue_request_storage)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_requests"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenueRequestStorageForm(instance=venue_request_storage)
        
    context = {
        "form": form,
    }
    return render(request, 'admin/pages/venue/request_storage/add_update.html', context)


@login_required(login_url='login')
@user_is_admin
def admin_delete_venue_request_storage(request, request_storage_id):
    try:
        handle_request_storage.delete_venue_request_storage(request_storage_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_venue_requests")) 


class VenuePicturesListView(LoginRequiredMixin, ListView):
    
    model = VenuePictures
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/venue/pictures/all.html"
    context_object_name = 'pictures'



@login_required(login_url='login')
@user_is_admin
def add_new_venue_picture(request):
    if request.method == 'POST':
        form = VenuePictureForm( request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_pictures"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenuePictureForm()
    return render(request, 'admin/pages/venue/pictures/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_venue_picture(request, picture_id):
    
    venue_picture = handle_venue_picture.get_venue_picture_by_id(picture_id)
    if request.method == 'POST':
        form = VenuePictureForm( request.POST, request.FILES, instance=venue_picture)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_venue_pictures"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = VenuePictureForm(instance=venue_picture)
        
    context = {
        "form": form,
    }
    return render(request, 'admin/pages/venue/pictures/add_update.html', context)


@login_required(login_url='login')
@user_is_admin
def admin_delete_venue_picture(request, picture_id):
    try:
        handle_venue_picture.delete_venue_picture(picture_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_venue_pictures")) 

