from django.urls import path
from UserManagement import views

app_name = 'UserManagement'

urlpatterns = [
    path('', views.index, name='index'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path("check-user/", views.check_user, name="check_user"),

    path('Administrator/', views.Administrator, name='Administrator'),

    path('Basicuser', views.Basicuser, name='Basicuser')
]