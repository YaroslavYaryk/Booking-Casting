
from customer.models import (Customer, CustomerAccess, CustomerContacts,
                             CustomerRequestsStorage)
from event.models import Event
from users.models import User
from users.services import user_handle


def get_customer_by_id(customer_id):
    return Customer.objects.get(pk=customer_id)

def get_customer_by_name(name):
    return Customer.objects.get(name=name)


def is_allowed_to_change(customer_id, user):
    customer = get_customer_by_id(customer_id)
    customer_access_obj = CustomerAccess.objects.get(customer=customer, access = user)
    return customer_access_obj.admin


def get_users_have_access(customer_id, user):
    
    customer = get_customer_by_id(customer_id)
    return CustomerAccess.objects.filter(customer=customer).exclude(access =user)


def get_customer_access_by_id(id):
    return CustomerAccess.objects.get(pk=id)

def delete_customer_access(access_id):
    get_customer_access_by_id(access_id).delete()
    

def get_customers_for_user(user):
    
    return CustomerAccess.objects.filter(access = user)


def add_user_can_change(customer, user_added):
    
    CustomerAccess.objects.create(customer=customer, access=user_added, admin=True)


def hash_info(data):
        
    name = data["name"]
    address = data["address"]
    zip_code = data["zip_code"]
    return hash(f"{name}{address}{zip_code}")


def get_or_create_customer_by_id(customer_id):
    
    customer = get_customer_by_id(customer_id)
    return CustomerContacts.objects.get_or_create(customer=customer)[0]


def contacts_exists(c_c):
    """ checks if main data filled """
    return c_c.first_name or c_c.last_name or c_c.phone or c_c.email or c_c.role or c_c.birthdate


def delete_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    customer.delete()


def delete_from_changeble(customer_id, user_id):
    
    customer = get_customer_by_id(customer_id)
    user = user_handle.get_user_by_id(user_id)
    try:
        CustomerAccess.objects.get(customer=customer, access=user).delete()
    except Exception as ex:
        print(ex)    


def get_customer_contacts_by_id(customer_contacts_id):
    return CustomerContacts.objects.get(pk=customer_contacts_id)


def delete_customer_contacts(customer_contacts_id):
    return get_customer_contacts_by_id(customer_contacts_id).delete()


def get_avaluable_users(customer):
    
    taken_users = [us.access.email for us in CustomerAccess.objects.filter(customer=customer)]
    taken_users += [us.email for us in User.objects.filter(admin=True)]
    print(User.objects.exclude(email__in = taken_users))
    return User.objects.exclude(email__in = taken_users)


def add_permission_to_change(customer_id, user_email, perm_type):
    
    customer = get_customer_by_id(customer_id)
    user = User.objects.get(email=user_email)
    customer_access = CustomerAccess.objects.filter(customer=customer, access=user)
    if customer_access:
        raise Exception("Can't add user that already exists")
    perm_type_py = True if perm_type == 'true' else False
    if perm_type_py:
        CustomerAccess.objects.create(customer = customer, access=user, admin=True)
    else:
        CustomerAccess.objects.create(customer = customer, access=user)


def change_permission_to_change(access_id, perm_type, user):
    
    customer_access_obj = CustomerAccess.objects.get(pk=access_id)
    perm_type_py = True if perm_type == 'true' else False
    
    if perm_type_py and customer_access_obj.admin != perm_type_py:
        storage = CustomerRequestsStorage.objects.filter(requester=customer_access_obj.access, owner=user, customer=customer_access_obj.customer)
        if storage:
            storage_obj = storage.first()
            storage_obj.granted = True
            storage_obj.done = True
            storage_obj.save()
            CustomerRequestsStorage.objects.filter(requester=customer_access_obj.access, customer=customer_access_obj.customer).exclude(owner=user).delete()
    
    if customer_access_obj.admin != perm_type_py:
        customer_access_obj.admin = perm_type_py
        customer_access_obj.save()
        
    
    return customer_access_obj.customer
    
    
    
def get_customer_request_storage_by_id(request_storage_id):
    return CustomerRequestsStorage.objects.get(pk=request_storage_id)


def delete_customer_request_storage(request_storage_id) :
    get_customer_request_storage_by_id(request_storage_id).delete()


def get_my_events(customer_id):
    return Event.objects.filter(customer__id=customer_id)
