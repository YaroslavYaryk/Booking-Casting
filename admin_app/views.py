from django.shortcuts import render

from admin_app.decorators import user_is_admin


# Create your views here
@user_is_admin
def index(request):
    return render(request, "admin/pages/dashboard.html")
