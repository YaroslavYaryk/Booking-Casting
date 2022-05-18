from customer.models import CustomerAccess, CustomerRequestsStorage
from django.db.models import Q
from users.services import user_handle

from .handle_customer import get_customer_by_id


def send_request(user, customer_id):
    customer = get_customer_by_id(customer_id)
    
    user_access_obj = CustomerAccess.objects.filter(customer=customer, admin=True)
    if user_access_obj:
        for access_user in user_access_obj:
            CustomerRequestsStorage.objects.create(requester = user, 
                                                 owner = access_user.access, 
                                                 customer = customer)

def get_customer_messages_for_user(user):
    
    messages = CustomerRequestsStorage.objects.filter(Q(requester=user) | Q(owner=user)).order_by("-created_at")
    return messages


def handle_request_form(r_from, r_to, customer_id, granted):
    print("worked")
    requester = user_handle.get_user_by_id(r_from)
    owner = user_handle.get_user_by_id(r_to)
    customer = get_customer_by_id(customer_id)
    deal = CustomerRequestsStorage.objects.get(requester = requester, owner = owner, customer = customer)
    if granted:
        customer.user.add(requester)
        deal.granted = True
        
    deal.done = True        
    deal.save()
