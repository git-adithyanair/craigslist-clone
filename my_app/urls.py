from django.urls.conf import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("new_search", views.new_search, name="new_search"),
]