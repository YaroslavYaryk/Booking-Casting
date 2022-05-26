# Create your views here.
from artist.decorators import user_has_perm_to_change
from customer.services import handle_customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from users.services import user_actions, user_handle

from company.models import Company
from company.services import handle_company

from .forms import CompanyForm, TermsForm


@method_decorator(user_has_perm_to_change, name="dispatch")
class CompanyListView(LoginRequiredMixin, ListView):

    model = Company
    # paginate_by = 100  # if pagination is desired
    template_name = "company/list.html"
    context_object_name = "companies"

    def get_queryset(self):
        return Company.objects.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_perm"] = self.request.user.is_staff
        return context


@login_required(login_url="login")
@user_has_perm_to_change
def add_new_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():
            company_obj = form.save()
            company_obj.creator = request.user
            company_obj.save()
            return HttpResponseRedirect(
                reverse(
                    "get_company_details",
                    kwargs={
                        "company_id": company_obj.id,
                    },
                )
            )
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CompanyForm()
    return render(request, "company/add_company.html", {"form": form})


@login_required(login_url="login")
@user_has_perm_to_change
def get_company_details(request, company_id):

    try:
        handle_company.is_allowed_to_change(company_id, request.user)
    except:
        return render(request, "dashboard/page_blocked.html")

    company = handle_company.get_company_by_id(company_id)
    context = {
        "company": company,
    }

    return render(request, "company/details.html", context=context)


@login_required(login_url="login")
def change_company_details(request, company_id):

    company = handle_company.get_company_by_id(company_id)
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    "get_company_details",
                    kwargs={
                        "company_id": company_id,
                    },
                )
            )
        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = CompanyForm(instance=company)
    return render(request, "company/edit_company.html", {"form": form})


@login_required(login_url="login")
def delete_company(request, company_id):

    try:
        handle_company.delete_company(company_id)
    except Exception as ex:
        print(ex)
    return HttpResponseRedirect(reverse("get_my_companies"))


def get_all_company_events(request, company_id):

    my_events = handle_company.get_my_events(company_id)
    context = {"events": my_events}

    return render(request, "company/company_events.html", context=context)


def load_company_terms(request, company_id):

    company = handle_company.get_company_by_id(company_id)

    if request.method == "POST":
        form = TermsForm(company.terms, request.POST)
        if form.is_valid():
            company.terms = request.POST["terms"]
            company.save()
            return HttpResponseRedirect(
                reverse(
                    "get_company_details",
                    kwargs={
                        "company_id": company_id,
                    },
                )
            )

        else:
            messages.error(request, "Opps, there are some problems")
    else:
        form = TermsForm(company.terms)

    return render(request, "company/terms.html", {"company": company, "form": form})
