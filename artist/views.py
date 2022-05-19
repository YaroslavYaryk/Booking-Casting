from multiprocessing import context

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
from users.services import user_actions, user_handle
from venue.services import handle_venue

from .decorators import user_has_perm_to_change
from .forms import ArtistAddForm, ArtistAssetsForm, RequestForm
from .models import Artist, ArtistAccess
from .services import request_user_to_change, user_artists


class MyArtistListView(LoginRequiredMixin, ListView):
    
    model = ArtistAccess
    # paginate_by = 100  # if pagination is desired
    template_name = "artist/my_artisis_list.html"
    context_object_name = 'artistsAccess'
    
    def get_queryset(self):
        # return Artist.objects.
        return user_artists.get_artists_for_user(self.request.user)
    
    def dispatch(self, *args, **kwargs):
        dispatch_method = super(MyArtistListView, self).dispatch

        if not (self.request.user.is_staff or  ArtistAccess.objects.filter(access = self.request.user)):
            raise PermissionDenied
        
        return dispatch_method(*args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_perm"] = self.request.user.is_staff
        return context

@login_required(login_url='login')
@user_has_perm_to_change
def add_new_artist(request):
    if request.method == 'POST':
        form = ArtistAddForm( request.POST)

        if form.is_valid():
            artist = form.save()
            try:
                user_artists.add_artist_access(artist, request.user)
                artist.save()
            except Exception as er:
                print(er)
            return HttpResponseRedirect(reverse("artist_details", kwargs={
                        "artist_id": artist.id,
                    },)) 
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAddForm()
    return render(request, 'artist/add_artist.html', {'form': form})


@login_required(login_url='login')
def get_artist_details(request, artist_id):
    try:
        user_artists.is_allowed_to_change(artist_id, request.user)
    except Artist.DoesNotExist:
        return render(request, "admin/404.html")
    except Exception as er:
        return render(request, "dashboard/page_blocked.html")
    
    artist_assets = user_artists.get_artist_assets(artist_id)
    if request.method == "POST":
        
        if not user_artists.is_allowed_to_change(artist_id, request.user):
            raise PermissionDenied
        
        try:
            print(request.POST)
            user_artists.save_artist_assets(artist_assets, request.POST.get("credit"), request.FILES)
            return HttpResponseRedirect(reverse("artist_details", kwargs={
                        "artist_id": artist_id,
                    },))
        except Exception as ex:
            raise ex
    try:
        artist = user_artists.get_artist_by_id(artist_id)
    except:
        artist = None
        
 
    context = {
        "artist" : artist,
        "is_allowed_to_change" : user_artists.is_allowed_to_change(artist_id, request.user),
        "artist_assets": artist_assets,
        "artist_files" : artist_assets.file.all(),
        "users_has_access" : user_artists.get_users_have_access(artist_id, request.user),
        "aval_users": user_artists.get_avaluable_users(artist),
        "my_events" : user_artists.get_my_events(artist_id)[:5]
    }
    
    return render(request, 'artist/artist_detailes.html', context=context)


@login_required(login_url='login')
def change_details_artist(request, artist_id):
    
    if not user_artists.is_allowed_to_change(artist_id, request.user):
        raise PermissionDenied
    
    artist = user_artists.get_artist_by_id(artist_id)
    if request.method == 'POST':
        form = ArtistAddForm( request.POST, instance=artist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("artist_details", kwargs={
                        "artist_id": artist_id,
                    },)) 
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAddForm(instance=artist)
    return render(request, 'artist/change_artist.html', {'form': form})


@login_required(login_url='login')
def send_request_to_change_artist(request, artist_id):
    user = request.user
    try:
        request_user_to_change.send_request(user, artist_id)
    except Exception as ex:
        print(ex)
        messages.error(request, ex)

    return HttpResponseRedirect(reverse("get_all_messages")) 


@login_required(login_url='login')
def get_all_messages(request):
    artist_messages = request_user_to_change.get_artist_messages_for_user(request.user)
    customer_messages = get_customer_messages_for_user(request.user)
    venue_messages = handle_venue.get_all_messages_for_user(request.user)
    context = {
        "artist_messages" : artist_messages,
        "customer_messages": customer_messages,
        "venue_messages": venue_messages
    }
    
    return render(request, "dashboard/all_messages.html", context=context)


@login_required(login_url='login')
def handle_change_request(request, r_from, r_to, artist_id):
    
    if request.method == 'POST':
        form = RequestForm( request.POST)
        if form.is_valid():
            choice = request.POST.get("choice")
            granted = list(request.POST.keys())[-1] == "accept"
            try:
                request_user_to_change.handle_request_form(r_from, r_to, artist_id, choice, granted )
            except Exception as ex:
                print(ex)
                messages.success(request, 'Something went wrong')
            return HttpResponseRedirect(reverse("home"))
            
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        print("get")
        form = RequestForm()
    
    context = {
        "form" : form,
        "requester": user_handle.get_user_by_id(r_from),
        "owner" : user_handle.get_user_by_id(r_to),
        "artist" : user_artists.get_artist_by_id(artist_id),
        "is_choice" : True,
        "body" : "artist"
    }
        
    return render(request, "dashboard/handle_request.html", context=context)

@login_required(login_url='login')
def delete_artist(request, artist_id):
    
    if not  user_artists.is_allowed_to_change(artist_id, request.user):
        print("here")
        raise PermissionDenied
    try:
        user_artists.delete_artist(artist_id) 
    except Exception as ex: 
        print(ex)
        messages.error(request, "Something went wrong")       
        
    if not (request.user.is_staff or  ArtistAccess.objects.filter(access = request.user)):
            return HttpResponseRedirect(reverse("home"))
    return HttpResponseRedirect(reverse("all_my_actors")) 


@login_required(login_url='login')
def delete_artist_file(request, artist_id, file_id):
    
    try:
        user_artists.delete_artist_file(file_id)
    except Exception as ex:
        print(ex)
    
    return HttpResponseRedirect(reverse("artist_details", kwargs={
                        "artist_id": artist_id,
                    },))


@login_required(login_url='login')
def delete_user_from_changeble(request, artist_id, user_id):
    
    try:
        user_artists.delete_from_changeble(artist_id, user_id)
    except Exception as ex:
        print(ex)
        messages.error(request, "Something went wrong")
        
    return HttpResponseRedirect(reverse("artist_details", kwargs={
                        "artist_id": artist_id,
                    },)) 


@login_required(login_url='login')
def add_user_permission_to_change_or_see(request, artist_id, user_email, perm_type):
    
    try:
        user_artists.add_permission_to_change(artist_id, user_email, perm_type)
    except Exception as er:
        print(er)
        # if er == "Can't add user that already exists":
        messages.error(request, er)
        # messages.error(request, "Something went wrong")
    
    return HttpResponseRedirect(reverse("artist_details", kwargs={
                        "artist_id": artist_id,
                    },))


@login_required(login_url='login')
def change_user_permission_to_change_or_see(request, access_id, perm_type):
    artist=""
    try:
        artist = user_artists.change_permission_to_change(access_id, perm_type, request.user)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")
        
    return HttpResponseRedirect(reverse("artist_details", kwargs={
                        "artist_id": artist.id,
                    },))


def get_all_artist_events(request, artist_id):
    
    my_events = user_artists.get_my_events(artist_id)
    context = {
        "events" : my_events
    }
    
    return render(request, "artist/artist_events.html", context=context)
