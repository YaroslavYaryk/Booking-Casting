from users.models import User, UserAbilities
from customer.models import CustomerAccess


def get_user_by_id(user_id):
    return User.objects.get(pk=user_id)


def get_user_by_name(name):
    return User.objects.get(name=name)


def get_user_ability_by_id(ability_id):
    return UserAbilities.objects.get(pk=ability_id)


def get_user_by_email(us_email):
    try:
        return User.objects.get(email=us_email)
    except Exception:
        pass


def get_user_by_phone(phone):
    return User.objects.get(phone=phone)


def filter_user_email(user_email):
    return User.objects.filter(email=user_email)


def is_allowed_to_create_contract(user_id):
    return CustomerAccess.objects.get(access__id=user_id, admin=True)
