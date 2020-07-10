from django.urls import path

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("home/", views.home, name="home"),
path("profile/", views.profile, name="profile"),
path("profile/account/", views.accountSettings, name="account"),
path('all/', views.AllView.as_view(), name='all'),
]