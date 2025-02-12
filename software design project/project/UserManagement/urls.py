from django.urls import path
from UserManagement import views

app_name = 'UserManagement'

urlpatterns = [
    # index URL
    path('', views.index, name='index'),
    
    path('auth/login/', views.microsoft_login, name='microsoft_login'),  # Redirect to Microsoft
    path('auth/callback/', views.login_view, name='auth_callback'),

    # Administrator URL
    path('Administrator/', views.Administrator, name='Administrator'),

    # Basicuser URL
    path('Basicuser/', views.Basicuser, name='Basicuser'),

    # create, update, delete user URL to fetch data from Administrator page
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/', views.update_user, name='update_user'),
    path('delete-user/', views.delete_user, name='delete_user'),
]