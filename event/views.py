from artist.decorators import user_has_perm_to_change
from company.models import Company
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.list import ListView
from users.services import user_handle

from .forms import (EventArtistEditForm, EventArtistForm, EventForm,
                    EventProductEditForm, EventProductForm)
from .models import EventTeam
from .services import handle_event


class MyEventsListView(LoginRequiredMixin, ListView):
    
    model = EventTeam
    template_name = "event/my_events_list.html"
    context_object_name = 'event_team'
    
    def get_queryset(self):
        return handle_event.get_event_for_user(self.request.user)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_perm"] = self.request.user.is_staff
        return context

@login_required(login_url='login')
@user_has_perm_to_change
def add_new_event(request):
    company_queryset = handle_event.get_company_queryset(request.user)
    venue_queryset = handle_event.get_venue_queryset(request.user)
    customer_queryset = handle_event.get_customer_queryset(request.user)
    
    if request.method == 'POST':
        form = EventForm(company_queryset, venue_queryset, customer_queryset, request.POST)
        print(request.POST)
        if form.is_valid():
            event_obj = form.save()
            print(event_obj.date)
            try:
                event_obj.contract = handle_event.get_final_contract(event_obj)
                event_obj.save()
                handle_event.add_user_to_event_team(event_obj.id, request.user, "creator")
            except Exception as er:
                messages.error(request, er)
            return HttpResponseRedirect(reverse("get_event_details", kwargs={
                "event_id" : event_obj.id
            }))
        else:
            messages.error(request, 'Opps, there are some problems')
    
    else:
        form = EventForm(company_queryset=company_queryset, venue_queryset=venue_queryset, customer_queryset=customer_queryset)
    return render(request, 'event/add_new_event.html', {'form': form})


@login_required(login_url='login')
def get_event_details(request, event_id):
    
    try:
        handle_event.is_allowed_to_change(event_id, request.user)
    except:
        return render(request, "dashboard/page_blocked.html")
    
    if request.method == "POST":
        if not handle_event.is_allowed_to_change(event_id, request.user):
            raise PermissionDenied
        
        
        form = EventArtistForm( handle_event.get_active_artists(event_id), request.POST)
        if form.is_valid():
            event = handle_event.get_event_by_id(event_id)
            event_artist = form.save(commit=False)
            event_artist.event = event
            try:
                event_artist.save()
                event.contract = handle_event.get_final_contract(event)
                event.save()
            except Exception as er:
                messages.error(request, er)
            
            return HttpResponseRedirect(reverse("get_event_details", kwargs={
                "event_id" : event_id
            }))
            
        else:
            print("invalid")
    else:
        form = EventArtistForm(handle_event.get_active_artists(event_id))
    try:
        event = handle_event.get_event_by_id(event_id)
    except:
        event = None
    context = {
        "event" : event,
        "is_allowed_to_change" : handle_event.is_allowed_to_change(event_id, request.user),
        "users_in_team" : handle_event.get_users_team(event_id, request.user),
        "form" : form,
        "my_artists": handle_event.get_my_artists(request.user),
        "aval_users": handle_event.get_avaluable_users(event),
        "form" : EventProductForm()
    }
    
    return render(request, 'event/event_details.html', context=context)


@login_required(login_url='login')
@user_has_perm_to_change
def update_event(request, event_id):
    company_queryset = handle_event.get_company_queryset(request.user)
    venue_queryset = handle_event.get_venue_queryset(request.user)
    customer_queryset = handle_event.get_customer_queryset(request.user)
    event = handle_event.get_event_by_id(event_id)
    
    if request.method == 'POST':
        form = EventForm(company_queryset, venue_queryset, customer_queryset, request.POST, instance = event)
        if form.is_valid():
            event_obj = form.save()
            
            try:
                event_obj.contract = handle_event.get_final_contract(event_obj)
                event_obj.save()
            except Exception as er:
                messages.error(request, er)
            return HttpResponseRedirect(reverse("get_event_details", kwargs={
                "event_id" : event_obj.id
            }))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = EventForm(company_queryset=company_queryset, venue_queryset=venue_queryset, customer_queryset=customer_queryset, instance=event)
    return render(request, 'event/update_event.html', {'form': form})




@login_required(login_url='login')
def delete_event(request, event_id):
    
    if not handle_event.is_allowed_to_change(event_id, request.user):
        raise PermissionDenied
    try:
        handle_event.delete_event(event_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("get_all_events")) 

    
@login_required(login_url='login')
def delete_artist_from_event(request, event_id, artist_id):
    
    if not handle_event.is_allowed_to_change(event_id, request.user):
        raise PermissionDenied
    try:
        handle_event.delete_artist_from_event(event_id, artist_id)
        event = handle_event.get_event_by_id(event_id)
        event.contract = handle_event.get_final_contract(event)
        event.save() 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("get_event_artist_list", kwargs={"event_id" : event_id}))


@login_required(login_url='login')
def load_contract_for_event(request, event_id):
    
    event = handle_event.get_event_by_id(event_id)
    event_contract = event.contract
    
    return render(request, "event/contract_view.html", {"contract": event_contract, "event": event})
    
    
@login_required(login_url='login')
def get_event_artist_list(request, event_id):
    event_artists = handle_event.get_event_artists(event_id)
    event = handle_event.get_event_by_id(event_id)
    return render(request, "event/event_artists_list.html", {"artists": event_artists, "event":event})


@login_required(login_url='login')
def edit_event_artist(request, event_id, ev_artist_id):
    
    
    event_artist = handle_event.get_event_artist_by_id(ev_artist_id)
    
    if request.method == "POST":
        if not handle_event.is_allowed_to_change(event_id, request.user):
            raise PermissionDenied
        form = EventArtistEditForm(request.POST, instance=event_artist)
        if form.is_valid():
            try:
                form.save()
            except Exception as er:
                messages.error(request, er)
            
            return HttpResponseRedirect(reverse("get_event_artist_list", kwargs={
                "event_id" : event_id
            }))
            
        else:
            print("invalid")
    else:
        form = EventArtistEditForm(instance=event_artist)
    
    context = {
        "form" : form,
        "event_artist": event_artist
    }

    return render(request, "event/edit_event_artist.html", context=context)


@login_required(login_url='login')
def add_user_to_team(request, event_id):
    
    if request.method == 'POST':
        try:
            handle_event.add_user_to_team(event_id, request.POST.get("users_for_adding"), request.POST.get("users_for_adding_role"))
        except Exception as er:
            messages.error(request, er)
    
    return HttpResponseRedirect(reverse("get_event_details", kwargs={
                "event_id" : event_id
            }))


@login_required(login_url='login')
def edit_user_in_team(request, event_id, user_email, role):
    
    try:
        handle_event.update_user_in_team( event_id, user_email, role)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")
    
        
    return HttpResponseRedirect(reverse("get_event_details", kwargs={
                "event_id" : event_id
            }))


@login_required(login_url='login')
def delete_user_from_team(request, event_id, user_email):
    
    try:
        handle_event.delete_user_from_team( event_id, user_email)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")
    
        
    return HttpResponseRedirect(reverse("get_event_details", kwargs={
                "event_id" : event_id
            }))


@login_required(login_url='login')
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
                handle_event.add_event_rental_product(event_id, rental_product, price, count)
            except Exception as er:
                print(er)
                messages.error(request, "Something went wrong")
        else:
            messages.error(request, "Form is invalid")
        
    return HttpResponseRedirect(reverse("get_event_details", kwargs={
                "event_id" : event_id
            }))


@login_required(login_url='login')
def get_event_products_list(request, event_id):
    event_products = handle_event.get_event_products(event_id)
    event = handle_event.get_event_by_id(event_id)
    return render(request, "event/event_products_list.html", {"products": event_products, "event":event})


@login_required(login_url='login')
def delete_event_product(request, event_id, product_id):
    
    try:
        handle_event.delete_event_product(product_id)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")
    
    return HttpResponseRedirect(reverse("get_event_products_list", kwargs={
                "event_id" : event_id
            }))


@login_required(login_url='login')
def edit_event_product(request, event_id, product_id):
    
    product = handle_event.get_event_product_by_id(product_id)
    if request.method == "POST":
        
            try:
                print(request.POST, request.FILES)
                if not handle_event.validate_product(request.POST):
                    messages.error(request, "Form is invalid")
                    return HttpResponseRedirect(reverse("edit_event_product", kwargs={
                            "event_id" : event_id,
                            "product_id": product_id
                        }))
                name = request.POST["name"]
                picture = request.FILES.get("picture")
                price = request.POST["price"]
                count = request.POST["count"]
                
                rental_product = handle_event.update_rental_product(name, picture, product)
                handle_event.update_event_rental_product(product, rental_product, price, count)
            except Exception as er:
                raise(er)
                messages.error(request, "Something went wrong")
                
            return HttpResponseRedirect(reverse("get_event_products_list", kwargs={
                "event_id" : event_id
            }))
            
    context = {
            "product" : product
        }
    
    return render(request, "event/edit_event_product.html", context=context)
