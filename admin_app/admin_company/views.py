from admin_app.decorators import user_is_admin
from company.models import Company
from company.services import handle_company
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

from .forms import CompanyForm


class CompanyListView(LoginRequiredMixin, ListView):

    model = Company
    # paginate_by = 100  # if pagination is desired
    template_name = "admin/pages/company/all.html"
    context_object_name = "companies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required(login_url="login")
@user_is_admin
def add_new_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            company_obj = form.save()
            company_obj.creator = user_handle.get_user_by_email(request.POST["user"])
            company_obj.save()
            return HttpResponseRedirect(reverse("admin_get_all_companies"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CompanyForm()
    users = User.objects.all()
    return render(
        request, "admin/pages/company/add_update.html", {"form": form, "users": users}
    )


@login_required(login_url="login")
@user_is_admin
def change_details_company(request, company_id):

    company = handle_company.get_company_by_id(company_id)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin_get_all_companies"))
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CompanyForm(instance=company)
    return render(request, "admin/pages/company/update.html", {"form": form})


@login_required(login_url="login")
@user_is_admin
def delete_company(request, company_id):

    try:
        handle_company.delete_company(company_id)
    except Exception as ex:
        print(ex)
    return HttpResponseRedirect(reverse("admin_get_all_companies"))
