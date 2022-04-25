from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("cap0", views.cap0, name="cap0")
]