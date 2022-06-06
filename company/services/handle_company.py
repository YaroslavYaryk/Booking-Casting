from datetime import datetime, timedelta
from company.models import Company
from event.models import Event


def get_company_by_id(id):
    return Company.objects.get(pk=id)


def delete_company(company_id):
    get_company_by_id(company_id).delete()


def is_allowed_to_change(company_id, user):

    company = get_company_by_id(company_id)
    return company.creator == user


def get_company_contracts(company, date):
    return company.contract_set.filter(date=date, visible=True)


def get_all_company_contracts(company):
    return company.contract_set.filter(visible=True)


def get_company_hiden_contracts(company):
    return company.contract_set.filter(visible=False)


def get_upcoming_contracts(company, date):
    date_today_datetime = datetime.strptime(date, "%Y-%m-%d").date()
    date_to = str(date_today_datetime + timedelta(days=20))
    return company.contract_set.filter(date__gte=date, date__lte=date_to, visible=True)
