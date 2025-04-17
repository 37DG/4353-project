from django.urls import path
from ApprovalSystem import views
from django.conf import settings

app_name = 'ApprovalSystem'

urlpatterns = [
    # menu for request both form
    path('', views.RequestMenu, name='RequestMenu'),
    # Input Cougar ID URL
    path('UserinputCougarID/', views.UserinputCougarID, name='UserinputCougarID'),
    # Verify Cougar ID URL
    path('UserverifyCougarID/', views.UserverifyCougarID, name='UserverifyCougarID'),

    # public information form
    path('PublicInformation/', views.PublicInformation, name='PublicInformation'),
    # save public information form
    path('savePublicInfo/', views.savePublicInfo, name='savePublicInfo'),
    # submit public information form
    path('submitPublicInfo/', views.submitPublicInfo, name='submitPublicInfo'),
    # Finish public information form
    path('finishPublicInfo/', views.finishPublicInfo, name='FinishPublicInfo'),



    # Early withdraw form
    path('EarlyWithdrawal/', views.EarlyWithdrawal, name='EarlyWithdrawal'),
    # save Early withdraw form
    path('saveEarlyWithdrawal/', views.saveEarlyWithdrawal, name='saveEarlyWithdrawal'),
    # submit Early withdraw form
    path('submitEarlyWithdrawal/', views.submitEarlyWithdrawal, name='submitEarlyWithdrawal'),
    # Finish Early withdraw form
    path('finishEarlyWithdrawal/', views.finishEarlyWithdrawal, name='FinishEarlyWithdrawal'),



    # Graduate petition form
    path('GraduatePetition/', views.GraduatePetition, name='GraduatePetition'),
    # Get graduate petition pdf
    path('get_GraduatePetition_pdf/', views.get_GraduatePetition_pdf, name='get_GraduatePetition_pdf'),
    # Finish Graduate petition form
    path('finishGraduatePetition/', views.finishGraduatePetition, name='FinishGraduatePetition'),





    # Undergraduate transfer form
    path('UndergraduateTransfer/', views.UndergraduateTransfer, name='UndergraduateTransfer'),
    # Get graduate petition pdf
    path('get_UndergraduateTransfer_pdf/', views.get_UndergraduateTransfer_pdf, name='get_GraduatePetition_pdf'),
    # Finish Graduate petition form
    path('finishUndergraduateTransfer/', views.finishUndergraduateTransfer, name='FinishGraduatePetition'),
]