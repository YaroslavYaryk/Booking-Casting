from contract.models import Contract, ContractEventTeam


def get_event_for_user(user):
    contracts_ids = [
        el.contract.id for el in ContractEventTeam.objects.filter(user=user)
    ]
    return Contract.objects.filter(id__in=contracts_ids)
