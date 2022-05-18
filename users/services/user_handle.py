from users.models import User, UserAbilities


def get_user_by_id(user_id):
    return User.objects.get(pk=user_id)

def get_user_by_name(name):
    return User.objects.get(name=name)


def get_user_ability_by_id(ability_id):
    return UserAbilities.objects.get(pk=ability_id)

def get_user_by_email(us_email):
    return User.objects.get(email=us_email)
