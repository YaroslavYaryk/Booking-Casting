from company.models import Company
from event.models import Event


def get_company_by_id(id):
    return Company.objects.get(pk=id)


def delete_company(company_id):
    get_company_by_id(company_id).delete()


def is_allowed_to_change(company_id, user):

    company = get_company_by_id(company_id)
    return company.creator == user
