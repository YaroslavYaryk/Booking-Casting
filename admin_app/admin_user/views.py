from admin_app.decorators import user_is_admin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.list import ListView
from users.models import User, UserAbilities
from users.services import user_actions, user_handle

from .forms import (PasswordChangeForm, UserAbilitiesForm, UserForm,
                    UserUpdateForm)
from .services import handle_user_admin


class UserListView(LoginRequiredMixin, ListView):

    model = User
    template_name = "admin/pages/users/user/all.html"
    context_object_name = 'users'



@login_required(login_url='login')
@user_is_admin
def add_new_user(request):
    if request.method == 'POST':
        form = UserForm( request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return HttpResponseRedirect(reverse("admin_get_all_users"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = UserForm()
    return render(request, 'admin/pages/users/user/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_user(request, user_id):
    
    user = user_handle.get_user_by_id(user_id)
    if request.method == 'POST':
        form = UserUpdateForm( request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_users"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'admin/pages/users/user/add_update.html', {'form': form, "type": "update", "uss": user})


@login_required(login_url='login')
@user_is_admin
def admin_change_user_password(request, user_id):
    user = user_handle.get_user_by_id(user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            try:
                handle_user_admin.change_user_password_admin(request.POST, user)
            except Exception as er:
                print(er)
            update_session_auth_hash(request, user)  # Important!
            return HttpResponseRedirect(reverse("admin_change_details_user",kwargs={
                        "user_id": user_id,
                    },))
        else:
            print("form invalid")
    else:
        form = PasswordChangeForm()
    return render(request, 'admin/pages/users/user/new_password.html', {'form': form})

@login_required(login_url='login')
@user_is_admin
def admin_delete_user(request, user_id):

    try:
        handle_user_admin.delete_user(user_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_users")) 



class UserAbilitiesListView(LoginRequiredMixin, ListView):
    
    model = UserAbilities
    template_name = "admin/pages/users/users_abilities/all.html"
    context_object_name = 'abilities'



@login_required(login_url='login')
@user_is_admin
def add_new_user_ability(request):
    if request.method == 'POST':
        form = UserAbilitiesForm( request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_user_abilities"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = UserAbilitiesForm()
    return render(request, 'admin/pages/users/users_abilities/add_update.html', {'form': form})



@login_required(login_url='login')
@user_is_admin
def change_details_user_abilities(request, ability_id):
    
    user_ability = user_handle.get_user_ability_by_id(ability_id)
    if request.method == 'POST':
        form = UserAbilitiesForm( request.POST, instance=user_ability)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_user_abilities"))
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = UserAbilitiesForm(instance=user_ability)
    return render(request, 'admin/pages/users/users_abilities/add_update.html', {'form': form, "type": "update",})


@login_required(login_url='login')
@user_is_admin
def admin_delete_user_ability(request, ability_id):

    try:
        handle_user_admin.delete_user_ability(ability_id) 
    except Exception as ex: 
        print(ex)       
    return HttpResponseRedirect(reverse("admin_get_all_user_abilities")) 



