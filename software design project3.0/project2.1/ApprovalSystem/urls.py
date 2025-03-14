from django.urls import path
from ApprovalSystem import views
from django.conf import settings

app_name = 'ApprovalSystem'

urlpatterns = [
    # menu for request both form
    path('', views.RequestMenu, name='RequestMenu'),

    # public information form
    path('PublicInformation/', views.PublicInformation, name='PublicInformation'),
    # save public information form
    path('savePublicInfo/', views.savePublicInfo, name='savePublicInfo'),
    # submit public information form
    path('submitPublicInfo/', views.submitPublicInfo, name='submitPublicInfo'),
    # Finish public information form
    path('finishPublicInfo/', views.finishPublicInfo, name='FinishPublicInfo'),



    # Early withdraw form
    path('EarlyWithdrawal/', views.EarlyWithdrawal, name='EarlyWithdraw'),
    # save Early withdraw form
    path('saveEarlyWithdrawal/', views.saveEarlyWithdrawal, name='saveEarlyWithdrawal'),
    # submit Early withdraw form
    path('submitEarlyWithdrawal/', views.submitEarlyWithdrawal, name='submitEarlyWithdrawal'),
    # Finish Early withdraw form
    path('finishEarlyWithdrawal/', views.finishEarlyWithdrawal, name='FinishEarlyWithdrawal'),
]