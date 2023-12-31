"""
URL configuration for Acc_route project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from users import views


urlpatterns = [
    path("", index, name="accueil"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("data/", data, name="data"),
    path("dashboard/", dashboard, name="dashboard"),
    path("data_pred/", data_predict, name="data_pred"),
    path("prediction/", predict, name="prediction"),
    path("404/", error_404, name="error_404"),
    path("about/", about, name="about"),
    path("admin/", admin.site.urls),
]
