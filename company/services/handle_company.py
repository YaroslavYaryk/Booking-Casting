from datetime import datetime, timedelta
from os import access
from company.models import Company, CompanyAccess
from event.models import Event


def get_company_by_id(id):
    return Company.objects.get(pk=id)


def delete_company(company_id):
    get_company_by_id(company_id).delete()


def get_company_for_user(user):
    company_ids = [el.company.id for el in CompanyAccess.objects.filter(access=user)]
    return Company.objects.filter(id__in=company_ids)


def is_allowed_to_see(company_id, user):
    return CompanyAccess.objects.get(company__id=company_id, access=user)


def get_company_contracts(company, date):
    return company.contract_set.filter(date=date, visible=True)


def get_all_company_contracts(company):
    return company.contract_set.filter(visible=True)


def get_company_hiden_contracts(company):
    return company.contract_set.filter(visible=False)


def get_upcoming_contracts(company, date):
    date_today_datetime = datetime.strptime(date, "%Y-%m-%d").date()
    date_from = str(date_today_datetime + timedelta(days=1))
    date_to = str(date_today_datetime + timedelta(days=20))
    return company.contract_set.filter(
        date__gte=date_from, date__lte=date_to, visible=True
    )


def add_user_to_company_access(company_obj, user, admin):
    CompanyAccess.objects.create(company=company_obj, access=user, admin=admin)


def get_users_have_access(company, user):
    return CompanyAccess.objects.filter(company=company).exclude(access=user)


def change_permission_to_change(access_id, perm_type, user):
    company_access_obj = CompanyAccess.objects.get(pk=access_id)
    perm_type_py = True if perm_type == "true" else False

    if company_access_obj.admin != perm_type_py:
        company_access_obj.admin = perm_type_py
        company_access_obj.save()

    return company_access_obj.company


def delete_from_changeble(access_id):
    company_access = CompanyAccess.objects.get(id=access_id)
    company = company_access.company
    company_access.delete()
    return company
