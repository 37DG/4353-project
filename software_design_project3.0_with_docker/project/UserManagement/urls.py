from django.urls import path
from UserManagement import views

#from rest_framework.routers import DefaultRouter
#from .views import UserViewSet

#router = DefaultRouter()
#router.register(r'api/users', UserViewSet)
#router.urls +  to 13

app_name = 'UserManagement'

urlpatterns = [
    # index URL
    path('', views.index, name='index'),
    
    path('auth/login/', views.microsoft_login, name='microsoft_login'),  # Redirect to Microsoft
    path('auth/logout/', views.logout_view, name='logout'),  # Logout URL
    path('auth/callback/', views.login_view, name='auth_callback'),

    #profile URL
    path('profile/', views.profile, name='profile'),

    # Deactivate user URL
    path('Deactivated_User/', views.Deactivated_User, name='Deactivated_User'),

    # Administrator URL
    path('Administrator/', views.Administrator, name='Administrator'),

    # Basicuser URL
    path('Basicuser/', views.Basicuser, name='Basicuser'),

    # change username URL
    path('changeUsername/', views.changeUsername, name='changeUsername'),

    # create, update, delete user URL to fetch data from Administrator page
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/', views.update_user, name='update_user'),
    path('delete-user/', views.delete_user, name='delete_user'),


    # Pending
    path('PublicInformationPending/', views.PublicInformationPending, name='ReleasePublicInformationPending'),
    path('EarlyWithdrawalPending/', views.EarlyWithdrawalPending, name='EarlyWithdrawalPending'),

    # view pending
    path('ViewPending/', views.ViewPending, name='ViewPending'),

    # Return the pending and ask user to remodify
    path('ReturnPending/', views.ReturnPending, name='ReturnPending'),
    # Approve the pending and change the note and status to user
    path('ApprovePending/', views.ApprovePending, name='ApprovePending'),


    ####################################################################
    # For other forms
    # other Pending
    path('GraduatePetitionPending/', views.GraduatePetitionPending, name='GraduatePetitionPending'),
    path('UndergraduateTransferPending/', views.UndergraduateTransferPending, name='UndergraduateTransferPending'),
    # new view pending
    path('newViewPending/', views.newViewPending, name='newViewPending'),
    # new Return the pending and ask user to remodify
    path('newReturnPending/', views.newReturnPending, name='newReturnPending'),
    # new Approve the pending and change the note and status to user
    path('newApprovePending/', views.newApprovePending, name='newApprovePending'),
]