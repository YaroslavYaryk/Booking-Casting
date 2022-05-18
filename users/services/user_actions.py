from users.models import UserAbilities


def get_all_abilities(user):
    return UserAbilities.objects.filter(user=user)


def create_ability(user, ability):
    UserAbilities.objects.create(user=user, ability=ability)


def delete_ability(user, ability_id):
    UserAbilities.objects.get(user=user, pk=ability_id).delete()

