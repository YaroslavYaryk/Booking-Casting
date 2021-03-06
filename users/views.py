from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from .forms import ChangeForm, LoginUserForm, RegisterUserForm
from .models import User
from .services import user_actions, user_handle
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext


@login_required(login_url="login")
def index(request):

    if request.user.is_admin:
        return HttpResponseRedirect(reverse("admin_dashboard"))
    context = {
        "message1": _("You have access to create whatever you want"),
        "message2": _(
            "You can't create anything, just wait some time till admin add you permissions"
        ),
    }
    return render(request, "dashboard/index.html", context)


class RegisterUser(SuccessMessageMixin, CreateView):
    """Show register form"""

    form_class = RegisterUserForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("login")
    success_message = "User added successfully"
    error_message = "Registration error"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["title"] = "Registration"
        return context


class LoginUser(SuccessMessageMixin, LoginView):

    """Autorization class"""

    form_class = LoginUserForm
    template_name = "auth/login.html"
    error_message = "Something went wrong"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["title"] = "Sign in"
        return context


@login_required(login_url="/accounts/login")
def update_view(request):
    if request.method == "POST":
        form = ChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # print(request.POST, request.GET)
            try:
                form.save()
            except Exception as er:
                messages.error(request, er)
        else:
            pass

    else:
        form = ChangeForm(instance=request.user)
    context = {
        "form": form,
        "userActions": user_actions.get_all_abilities(request.user),
    }
    return render(request, "auth/update_profile.html", context)


@login_required(login_url="/accounts/login")
def user_profile_view(request, user_id):

    if request.user.id == int(user_id):
        return HttpResponseRedirect(reverse("update_user_data"))

    user = user_handle.get_user_by_id(user_id)

    context = {"userActions": user_actions.get_all_abilities(request.user), "us": user}
    return render(request, "auth/user_profile_view.html", context)


@login_required(login_url="/accounts/login")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Password changed successfully")
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Ups, noe gikk galt. Pr??v p?? nytt")

    else:
        form = PasswordChangeForm(request.user)
    return render(request, "auth/change_password.html", {"form": form})


class LogoutUser(LogoutView, SuccessMessageMixin):

    next_page = "home"
    success_message = "Logout successfully"


@login_required(login_url="/accounts/login")
def add_ability(request, *args, **kwargs):

    user_actions.create_ability(user=request.user, ability=kwargs.get("ability_value"))
    return HttpResponseRedirect(reverse("update_user_data"))


@login_required(login_url="/accounts/login")
def delete_ability(request, *args, **kwargs):

    user_actions.delete_ability(user=request.user, ability_id=kwargs.get("ability_id"))
    return HttpResponseRedirect(reverse("update_user_data"))


def handler_forbiden(request, exception):
    return render(request, "admin/403.html")


def load_blocked_page(request):
    return render(request, "dashboard/page_blocked.html")
