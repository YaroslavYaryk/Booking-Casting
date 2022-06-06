# Create your views here.
from datetime import datetime
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
from artist.services import user_artists, constants as artist_constants
from contract.services import handle_contract


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
        "my_contracts": handle_company.get_all_company_contracts(company),
        "today_today": str(datetime.today().date()),
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


@login_required(login_url="login")
def get_all_company_events(request, company_id):

    my_events = handle_company.get_my_events(company_id)
    context = {"events": my_events}

    return render(request, "company/company_events.html", context=context)


@login_required(login_url="login")
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


@login_required(login_url="login")
def get_company_contracts(request, company_id, date):

    company = handle_company.get_company_by_id(company_id)

    try:
        company_contracts = handle_company.get_company_contracts(company, date)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    context = {
        "company": company,
        "contracts": company_contracts,
        "today_date": date,
        "today_today": str(datetime.today().date()),
        "week_days_list": user_artists.get_week_days_list(
            datetime.strptime(date, "%Y-%m-%d").date(),
            artist_constants.week_names_count[
                datetime.strptime(date, "%Y-%m-%d").date().strftime("%A")
            ],
        ),
        "visible": True,
        "upcoming_contracts": handle_company.get_upcoming_contracts(company, date),
    }

    return render(request, "company/company_contracts.html", context)


@login_required(login_url="login")
def get_company_hiden_contracts(request, company_id):

    company = handle_company.get_company_by_id(company_id)

    try:
        company_contracts = handle_company.get_company_hiden_contracts(company)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    context = {
        "company": company,
        "contracts": company_contracts,
        "today_today": str(datetime.today().date()),
        "visible": False,
    }

    return render(request, "company/company_contracts.html", context)


@login_required(login_url="login")
def hide_artist_contract(request, contract_id, date):

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.hide_contract(contract)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_company_contracts",
            kwargs={"company_id": contract.company.id, "date": date},
        )
    )


@login_required(login_url="login")
def unhide_artist_contract(request, contract_id):

    contract = handle_contract.get_contract_artist_by_id(contract_id)
    try:
        handle_contract.unhide_contract(contract)
    except Exception as err:
        print(err)
        messages(request, "Something went wrong")

    return HttpResponseRedirect(
        reverse(
            "get_company_hiden_contracts",
            kwargs={"company_id": contract.company.id},
        )
    )
