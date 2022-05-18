from admin_app.decorators import user_is_admin
from artist.models import (Artist, ArtistAccess, ArtistAssets, ArtistFile,
                           ArtistRequestsStorage)
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
from users.models import User
from users.services import user_actions, user_handle

from .forms import (ArtistAccessForm, ArtistAddForm, ArtistAssetsForm,
                    ArtistFileForm, ArtistRequestStorageForm)


class ArtistListView(LoginRequiredMixin, ListView):

    model = Artist
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/artist/artist/all.html"
    context_object_name = 'artists'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required(login_url='login')
@user_is_admin
def add_new_artist(request):
    if request.method == 'POST':
        form = ArtistAddForm( request.POST)

        if form.is_valid():
            artist = form.save()
            try:
                user_artists.add_artist_access(artist, user_handle.get_user_by_email(request.POST["user"]))
                artist.save()
            except Exception as er:
                print(er)
            return HttpResponseRedirect(reverse("admin_get_all_artist"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAddForm()
        
    users = User.objects.all()
    return render(request, 'admin/pages/artist/artist/add_update.html', {'form': form, "users":users})



@login_required(login_url='login')
@user_is_admin
def change_details_artist(request, artist_id):
    
    artist = user_artists.get_artist_by_id(artist_id)
    if request.method == 'POST':
        form = ArtistAddForm( request.POST, instance=artist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_artist"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAddForm(instance=artist)
    return render(request, 'admin/pages/artist/artist/update.html', {'form': form})

@login_required(login_url='login')
@user_is_admin
def delete_artist(request, artist_id):

    try:
        user_artists.delete_artist(artist_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_artist")) 



class ArtisAccesstListView(LoginRequiredMixin, ListView):
    
    model = ArtistAccess
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/artist/access/all.html"
    context_object_name = 'access'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required(login_url='login')
@user_is_admin
def add_new_artist_access(request):
    if request.method == 'POST':
        form = ArtistAccessForm( request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_artist_access"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAccessForm()
    return render(request, 'admin/pages/artist/access/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_artist_access(request, access_id):
    
    artist_access = user_artists.get_artist_access_by_id(access_id)
    if request.method == 'POST':
        form = ArtistAccessForm( request.POST, instance=artist_access)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_artist_access"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAccessForm(instance=artist_access)
    return render(request, 'admin/pages/artist/access/add_update.html', {'form': form})


@login_required(login_url='login')
@user_is_admin
def admin_delete_artist_access(request, access_id):
    print("here")
    try:
        user_artists.delete_artist_access(access_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_artist_access")) 



class ArtistFilesListView(LoginRequiredMixin, ListView):
    
    model = ArtistFile
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/artist/file/all.html"
    context_object_name = 'files'



@login_required(login_url='login')
@user_is_admin
def add_new_artist_file(request):
    if request.method == 'POST':
        form = ArtistFileForm( request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_files"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistFileForm()
    return render(request, 'admin/pages/artist/file/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_artist_file(request, file_id):
    
    file = user_artists.get_file_by_id(file_id)
    if request.method == 'POST':
        form = ArtistFileForm( request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_files"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistFileForm(instance=file)
        
    context = {
        "form": form,
        "type": "update",
        "f": file
    }
    return render(request, 'admin/pages/artist/file/add_update.html', context)


@login_required(login_url='login')
@user_is_admin
def admin_delete_artist_file(request, file_id):
    print("here")
    try:
        user_artists.delete_artist_file(file_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_files")) 


class ArtistAssetsListView(LoginRequiredMixin, ListView):
    
    model = ArtistAssets
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/artist/assets/all.html"
    context_object_name = 'assets'



@login_required(login_url='login')
@user_is_admin
def add_new_artist_assets(request):
    if request.method == 'POST':
        form = ArtistAssetsForm( request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_artist_assets"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAssetsForm()
    return render(request, 'admin/pages/artist/assets/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_artist_assets(request, assets_id):
    
    artist_assets = user_artists.get_assets_by_id(assets_id)
    if request.method == 'POST':
        form = ArtistAssetsForm( request.POST, request.FILES, instance=artist_assets)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_artist_assets"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistAssetsForm(instance=artist_assets)
        
    context = {
        "form": form,
    }
    return render(request, 'admin/pages/artist/assets/add_update.html', context)


@login_required(login_url='login')
@user_is_admin
def admin_delete_artist_assets(request, assets_id):
    try:
        user_artists.delete_artist_assets(assets_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_artist_assets")) 



class ArtistRequestStorageListView(LoginRequiredMixin, ListView):
    
    model = ArtistRequestsStorage
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/artist/request_storage/all.html"
    context_object_name = 'requests'



@login_required(login_url='login')
@user_is_admin
def add_new_artist_request_storage(request):
    if request.method == 'POST':
        form = ArtistRequestStorageForm( request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_request_storage"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistRequestStorageForm()
    return render(request, 'admin/pages/artist/request_storage/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_artist_request_storage(request, request_storage_id):
    
    artist_request_storage = user_artists.get_artist_request_storage_by_id(request_storage_id)
    if request.method == 'POST':
        form = ArtistRequestStorageForm( request.POST, request.FILES, instance=artist_request_storage)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_request_storage"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = ArtistRequestStorageForm(instance=artist_request_storage)
        
    context = {
        "form": form,
    }
    return render(request, 'admin/pages/artist/request_storage/add_update.html', context)


@login_required(login_url='login')
@user_is_admin
def admin_delete_artist_request_storage(request, request_storage_id):
    try:
        user_artists.delete_artist_request_storage(request_storage_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_request_storage")) 

