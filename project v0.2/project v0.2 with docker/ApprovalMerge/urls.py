from django.urls import path
from ApprovalMerge import views
from django.conf import settings

app_name = 'ApprovalMerge'

urlpatterns = [
    # Graduate petition form
    path('GradPetition/', views.GradPetition, name='GradPetition'),
    # save Graduate petition form
    # path('saveGradPetition/', views.saveGradPetition, name='saveGradPetition'),
    # submit Graduate petition form
    path('submitGradPetition/', views.submitGradPetition, name='submitGradPetition'),
    # Finish Graduate petition form
    path('finishGradPetition/', views.finishGradPetition, name='FinishGradPetition'),
]