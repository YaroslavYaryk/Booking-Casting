from django.urls import path

from .views import index, EventUserList

urlpatterns = [
    path("", index),
    path("list/", EventUserList.as_view()),
]
