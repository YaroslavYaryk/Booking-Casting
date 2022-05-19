
from artist.decorators import user_has_perm_to_change
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.list import ListView
from users.services import user_handle

from .forms import CustomerAddForm, CustomerContactsAddForm
from .models import Customer, CustomerAccess
from .services import handle_customer, request_user_to_change


class CustomerListView(LoginRequiredMixin, ListView):

    model = Customer
    # paginate_by = 100  # if pagination is desired
    template_name = "customer/customer_list.html"
    context_object_name = 'customers'
    
    def get_queryset(self):
        return Customer.objects.filter(active=True)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_perm"] = self.request.user.is_staff
        return context


class MyCustomerListView(LoginRequiredMixin, ListView):
    
    model = CustomerAccess
    template_name = "customer/my_customer_list.html"
    context_object_name = 'customer_access'
    
    def get_queryset(self):
        print("its here")
        return handle_customer.get_customers_for_user(self.request.user)

    def dispatch(self, *args, **kwargs):
        dispatch_method = super(MyCustomerListView, self).dispatch
        if not (self.request.user.is_staff or  CustomerAccess.objects.filter(access = self.request.user)):
            raise PermissionDenied
        
        return dispatch_method(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_perm"] = self.request.user.is_staff
        return context

@login_required(login_url='login')
@user_has_perm_to_change
def add_new_customer(request):
    if request.method == 'POST':
        form = CustomerAddForm( request.POST)

        if form.is_valid():
            customer_obj = form.save()
            customer_obj.organization_number = handle_customer.hash_info(form.cleaned_data)
            
            try:
                handle_customer.add_user_can_change(customer_obj, request.user)
            except Exception as ex:
                print(ex)
            customer_obj.save()
            
            return HttpResponseRedirect(reverse("customer_details", kwargs={
                        "customer_id": customer_obj.id,
                    },)) 
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = CustomerAddForm()
    return render(request, 'customer/add_customer.html', {'form': form})

# HANDLE When user hasnt permission to change - he cant change or see form of user contacts 
# check if user contacts for thois customer is filled, otherway dont even display contact info


@login_required(login_url='login')
def get_customer_details(request, customer_id):
    
    try:
        handle_customer.is_allowed_to_change(customer_id, request.user)
    except:
        return render(request, "dashboard/page_blocked.html")
    
    
    customer_contacts = handle_customer.get_or_create_customer_by_id(customer_id)
    if request.method == "POST":
        
        form = CustomerContactsAddForm(request.POST, instance=customer_contacts)
        if form.is_valid():
           form.save()
    else:
        form = CustomerContactsAddForm(instance=customer_contacts)
    try:
        customer = handle_customer.get_customer_by_id(customer_id)
    except:
        customer = None
    print("here ----",handle_customer.is_allowed_to_change(customer_id, request.user))
    context = {
        "customer" : customer,
        "is_allowed_to_change" : handle_customer.is_allowed_to_change(customer_id, request.user),
        "users_have_access" : handle_customer.get_users_have_access(customer_id, request.user),
        "form" : form,
        "contacts_exists" : handle_customer.contacts_exists(customer_contacts),
        "customer_contacts" : customer_contacts,
        "aval_users": handle_customer.get_avaluable_users(customer),
        "my_events" : handle_customer.get_my_events(customer_id)[:5],
    }
    
    return render(request, 'customer/customer_details.html', context=context)


@login_required(login_url='login')
def change_details_customer(request, customer_id):
    
    if not handle_customer.is_allowed_to_change(customer_id, request.user):
        raise PermissionDenied
    
    customer = handle_customer.get_customer_by_id(customer_id)
    if request.method == 'POST':
        form = CustomerAddForm( request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("customer_details", kwargs={
                        "customer_id": customer_id,
                    },)) 
        else:
            messages.error(request, 'Opps, there are some problems')
    else:
        form = CustomerAddForm(instance=customer)
    return render(request, 'customer/change_customer.html', {'form': form})


@login_required(login_url='login')
def send_request_to_change_customer(request, customer_id):
    user = request.user
    try:
        request_user_to_change.send_request(user, customer_id)
    except Exception as ex:
        
        messages.error(request, ex)

    return HttpResponseRedirect(reverse("get_all_messages")) 



@login_required(login_url='login')
def handle_change_request(request, r_from, r_to, customer_id):
    
    if request.method == 'POST':
        granted = list(request.POST.keys())[-1] == "accept"
        try:
            request_user_to_change.handle_request_form(r_from, r_to, customer_id,  granted )
        except Exception as ex:
            print(ex)
            messages.success(request, 'Something went wrong')
        return HttpResponseRedirect(reverse("home"))
            
    else:
        print("get")
    
    context = {
        "requester": user_handle.get_user_by_id(r_from),
        "owner" : user_handle.get_user_by_id(r_to),
        "customer" : handle_customer.get_customer_by_id(customer_id),
        "is_choice" : False,
        "body" : "customer"
    }
        
    return render(request, "dashboard/handle_request.html", context=context)

@login_required(login_url='login')
def delete_customer(request, customer_id):
    
    if not handle_customer.is_allowed_to_change(customer_id, request.user):
        raise PermissionDenied
    try:
        handle_customer.delete_customer(customer_id) 
    except Exception as ex: 
        print(ex)       
        
    if not (request.user.is_staff or CustomerAccess.objects.filter(access = request.user)):
            return HttpResponseRedirect(reverse("home"))
    return HttpResponseRedirect(reverse("my_customers")) 


def delete_user_from_customer_changeble(request, customer_id, user_id):
    
    try:
        handle_customer.delete_from_changeble(customer_id, user_id)
    except Exception as ex:
        print(ex)
        
    return HttpResponseRedirect(reverse("customer_details", kwargs={
                        "customer_id": customer_id,
                    },)) 


@login_required(login_url='login')
def add_user_permission_to_change_or_see_customer(request, customer_id, user_email, perm_type):
    
    try:
        handle_customer.add_permission_to_change(customer_id, user_email, perm_type)
    except Exception as er:
        print(er)
        messages.error(request, er)
    
    return HttpResponseRedirect(reverse("customer_details", kwargs={
                        "customer_id": customer_id,
                    },))


@login_required(login_url='login')
def change_user_permission_to_change_or_see_customer(request, access_id, perm_type):
    customer=""
    try:
        customer = handle_customer.change_permission_to_change(access_id, perm_type, request.user)
    except Exception as er:
        print(er)
        messages.error(request, "Something went wrong")
    
    return HttpResponseRedirect(reverse("customer_details", kwargs={
                    "customer_id": customer.id,
                },))



def get_all_customer_events(request, customer_id):
    
    my_events = handle_customer.get_my_events(customer_id)
    context = {
        "events" : my_events
    }
    
    return render(request, "customer/customer_events.html", context=context)
