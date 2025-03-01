from django.urls import path
from Home import views

app_name = 'Home'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
]