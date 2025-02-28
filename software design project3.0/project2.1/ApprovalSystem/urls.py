from django.urls import path
from ApprovalSystem import views
from django.conf import settings

app_name = 'ApprovalSystem'

urlpatterns = [
    path('', views.RequestMenu, name='RequestMenu'),

    path('PublicInformation/', views.PublicInformation, name='PublicInformation'),

    path('EarlyWithdraw/', views.EarlyWithdraw, name='EarlyWithdraw'),
]