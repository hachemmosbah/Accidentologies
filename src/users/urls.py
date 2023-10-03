from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path("", login_view, name="login"),
   path("", signup, name="signup"),
   path("",logout_view, name="logout"),
]

