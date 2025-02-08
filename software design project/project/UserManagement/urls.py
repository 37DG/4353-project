from django.urls import path
from UserManagement import views

app_name = 'UserManagement'

urlpatterns = [
    # index URL
    path('', views.index, name='index'),

    # dashboard URL
    path('dashboard/', views.dashboard, name='dashboard'),

    # fetch user when user try to login from dashboard
    path("check-user/", views.check_user, name="check_user"),

    # Administrator URL
    path('Administrator/', views.Administrator, name='Administrator'),

    # Basicuser URL
    path('Basicuser/', views.Basicuser, name='Basicuser'),

    # create, update, delete user URL to fetch data from Administrator page
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/', views.update_user, name='update_user'),
    path('delete-user/', views.delete_user, name='delete_user'),
]
