from admin_app.decorators import user_is_admin
from artist.services import request_user_to_change, user_artists
from customer.services.request_user_to_change import \
    get_customer_messages_for_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.list import ListView
from event.models import (EventArtists, EventRentalProducts, EventTeam,
                          RentalProducts)
from event.services import handle_event
from users.models import User
from users.services import user_actions, user_handle

from .forms import (EventArtistForm, EventEditForm, EventForm,
                    EventRentalProductsForm, EventTeamForm, RentalProductsForm)


class MyEventsListView(LoginRequiredMixin, ListView):
    
    model = EventTeam
    template_name = "admin/pages/event/event/all.html"
    context_object_name = 'events'
    
    def get_queryset(self):
        return handle_event.get_all_events()



@login_required(login_url='login')
@user_is_admin
def add_new_event(request):
    
    if request.method == 'POST':
        form = EventForm( request.POST)
        print(request.POST)
        if form.is_valid():
            event_obj = form.save()
            try:
                event_obj.contract = handle_event.get_final_contract(event_obj)
                event_obj.save()
                handle_event.add_user_to_event_team(event_obj.id, 
                                                    user_handle.get_user_by_email(request.POST["user"]), 
                                                    "creator")
            except Exception as er:
                messages.error(request, er)
            return HttpResponseRedirect(reverse("admin_get_all_eevents"))
        else:
            messages.error(request, 'Opps, there are some problems')
    
    else:
        form = EventForm()
        
    users = User.objects.all()
    return render(request, 'admin/pages/event/event/add.html', {'form': form, "users":users})


@login_required(login_url='login')
@user_is_admin
def update_event(request, event_id):
    event = handle_event.get_event_by_id(event_id)
    
    if request.method == 'POST':
        form = EventEditForm(request.POST, instance = event)
        if form.is_valid():
            event_obj = form.save()
            
            try:
                event_obj.contract = handle_event.get_final_contract(event_obj)
                event_obj.save()
            except Exception as er:
                messages.error(request, er)
            return HttpResponseRedirect(reverse("admin_get_all_eevents"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventEditForm( instance=event)
    return render(request, 'admin/pages/event/event/update.html', {'form': form, "event":event})



@login_required(login_url='login')
@user_is_admin
def delete_event(request, event_id):

    try:
        handle_event.delete_event(event_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_eevents")) 



class EventTeamListView(LoginRequiredMixin, ListView):
    
    model = EventTeam
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/event/team/all.html"
    context_object_name = 'events'




@login_required(login_url='login')
@user_is_admin
def add_new_event_team(request):
    if request.method == 'POST':
        form = EventTeamForm( request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_event_teams"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventTeamForm()
    return render(request, 'admin/pages/event/team/add.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_event_team(request, event_team_id):
    
       
    event_team = handle_event.get_event_team_by_id(event_team_id)
    if request.method == 'POST':
        form = EventTeamForm( request.POST, instance=event_team)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_event_teams"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventTeamForm(instance=event_team)
    return render(request, 'admin/pages/event/team/update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def admin_delete_event_team(request, event_team_id):
    try:
        handle_event.delete_event_team(event_team_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_event_teams")) 



class EventArtistsListView(LoginRequiredMixin, ListView):
    
    model = EventArtists
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/event/artists/all.html"
    context_object_name = 'events_artists'




@login_required(login_url='login')
@user_is_admin
def add_new_event_artist(request):
    if request.method == 'POST':
        form = EventArtistForm( request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_events_artists"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventArtistForm()
    return render(request, 'admin/pages/event/artists/add.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_event_artist(request, event_artist_id):
    
       
    event_artist = handle_event.get_event_artist_by_id(event_artist_id)
    if request.method == 'POST':
        form = EventArtistForm( request.POST, instance=event_artist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_events_artists"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventArtistForm(instance=event_artist)
    return render(request, 'admin/pages/event/artists/update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def admin_delete_event_artist(request, event_artist_id):
    try:
        handle_event.delete_event_artist(event_artist_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_events_artists")) 



class RentalProductsView(LoginRequiredMixin, ListView):
    
    model = RentalProducts
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/event/rental_products/all.html"
    context_object_name = 'rental_products'


@login_required(login_url='login')
@user_is_admin
def add_new_rental_product(request):
    if request.method == 'POST':
        form = RentalProductsForm( request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_rental_products"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = RentalProductsForm()
    return render(request, 'admin/pages/event/rental_products/add.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_rental_product(request, rental_product_id):
    
       
    rental_product = handle_event.get_rental_product_by_id(rental_product_id)
    if request.method == 'POST':
        form = RentalProductsForm( request.POST, request.FILES, instance=rental_product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_rental_products"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = RentalProductsForm(instance=rental_product)
    return render(request, 'admin/pages/event/rental_products/update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def admin_delete_rental_product(request, rental_product_id):
    try:
        handle_event.delete_rental_product(rental_product_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_rental_products")) 



class EventRentalProductsView(LoginRequiredMixin, ListView):
    
    model = EventRentalProducts
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/event/event_rental_products/all.html"
    context_object_name = 'rental_products'


@login_required(login_url='login')
@user_is_admin
def add_new_event_rental_product(request):
    if request.method == 'POST':
        form = EventRentalProductsForm( request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_event_rental_products"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventRentalProductsForm()
    return render(request, 'admin/pages/event/event_rental_products/add.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_event_product(request, event_product_id):
    
       
    event_product = handle_event.get_event_rental_product_by_id(event_product_id)
    if request.method == 'POST':
        form = EventRentalProductsForm( request.POST, request.FILES, instance=event_product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_event_rental_products"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventRentalProductsForm(instance=event_product)
    return render(request, 'admin/pages/event/event_rental_products/update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def admin_delete_event_product(request, event_product_id):
    try:
        handle_event.delete_event_rental_product(event_product_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_event_rental_products")) 

