from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
import msal
import requests
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from UserManagement.models import User
from .models import Public_info, Early_withdrawal
from django.conf import settings

import os
import subprocess
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now

# Display the menu for the user to select the request type
def RequestMenu(request):
    user = {
        "email": User.objects.get(email=request.session.get("user_email")).email,
        "name": User.objects.get(email=request.session.get("user_email")).name,
        "role": User.objects.get(email=request.session.get("user_email")).role,
        "status": User.objects.get(email=request.session.get("user_email")).status,
    }

    return render(request, 'RequestMenu.html', {"user": user})

# Display the form for the user to fill in the public information request
def PublicInformation(request):
    user = {
        "email": User.objects.get(email=request.session.get("user_email")).email,
        "name": User.objects.get(email=request.session.get("user_email")).name,
        "role": User.objects.get(email=request.session.get("user_email")).role,
        "status": User.objects.get(email=request.session.get("user_email")).status,
    }

    try:
        record = Public_info.objects.get(email=user['email'])

        if record.status == 'draft' or record.status =='returned':
            return render(request, 'PublicInformation.html', {"user": user, "form_url": settings.MEDIA_URL, "record": record})
        elif record.status == 'pending':
            return render(request, 'WaitForPending.html', {"user": user})
        elif record.status == 'approved':
            pdf_filename = f"{record.name.replace(" ", "_")}_PublicInfo_{record.date.strftime('%Y-%m-%d_%H_%M_%S')}.pdf"
            return render(request, 'PublicInfoApproved.html', {"user": user, "pdf_filename": pdf_filename})
    except Public_info.DoesNotExist:
        return render(request, 'PublicInformation.html', {"user": user, "form_url": settings.MEDIA_URL})

# Feature for user to save the public information request
def savePublicInfo(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("full_name")
        option = request.POST.get("request_type")
        id = request.POST.get("id")
        signature = request.FILES.get("signature")

        newname = name.replace(" ", "_")
        form = 'PublicInfo'
        PublicInfo_signature_url = None
        if signature:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            file_extension = signature.name.split('.')[-1]
            signature_filename = f"{newname}_{form}.{file_extension}"
            file_path = os.path.join(settings.MEDIA_ROOT, signature_filename)

            # Delete the old file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)

            filename = fs.save(signature_filename, signature)

        Public_info.objects.update_or_create(
            email=email,
            defaults={
            'name':name,
            'option':option,
            'ID' :id,
            'date':now(),
            }
        )

        return redirect('http://localhost:8000/approvalsystem')

# Feature for user to submit the public information request
def submitPublicInfo(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("full_name")
        option = request.POST.get("request_type")
        id = request.POST.get("id")
        signature = request.FILES.get("signature")

        newname = name.replace(" ", "_")
        form = 'PublicInfo'
        PublicInfo_signature_url = None
        if signature:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            file_extension = signature.name.split('.')[-1]
            signature_filename = f"{newname}_{form}.{file_extension}"
            file_path = os.path.join(settings.MEDIA_ROOT, signature_filename)

            # Delete the old file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)

            filename = fs.save(signature_filename, signature)

        date = now()
        signature_path = file_path.replace('\\','/')

        Public_info.objects.update_or_create(
            email=email,
            defaults={
            'name':name,
            'option':option,
            'ID' :id,
            'date':date,
            'status': 'pending'
            }
        )

        # Run make file
        latex_path = os.path.abspath("Latex/")  # Path to Makefile
        pdf_basename = f"{newname}_{form}_{date.strftime('%Y-%m-%d_%H_%M_%S')}"
        if option == 'A':
            subprocess.run(["make", "buildPublicInfo", 
                            f"TEX_NAME=public_info.tex", 
                            f"PDFBASENAME={pdf_basename}", 
                            f"PUBLIC_INFO_OPTIONA={option}", 
                            f"PUBLIC_INFO_NAME={name}", 
                            f"PUBLIC_INFO_ID={id}", 
                            f"PUBLIC_INFO_DATE={date}", 
                            f"PUBLIC_INFO_SIGNATURE={signature_path}"], cwd=latex_path)
        elif option == 'B':
            subprocess.run(["make", "buildPublicInfo", 
                            f"TEX_NAME=public_info.tex", 
                            f"PDFBASENAME={pdf_basename}", 
                            f"PUBLIC_INFO_OPTIONB={option}", 
                            f"PUBLIC_INFO_NAME={name}", 
                            f"PUBLIC_INFO_ID={id}", 
                            f"PUBLIC_INFO_DATE={date}", 
                            f"PUBLIC_INFO_SIGNATURE={signature_path}"], cwd=latex_path)


        return render(request, 'WaitForPending.html', {"user": {'name':name}})


def finishPublicInfo(request):
    record = Public_info.objects.get(email=request.session.get("user_email"))
    record.status = 'draft'
    record.note = ''
    record.save()

    return redirect('http://localhost:8000/approvalsystem')











def EarlyWithdrawal(request):
    user = {
        "email": User.objects.get(email=request.session.get("user_email")).email,
        "name": User.objects.get(email=request.session.get("user_email")).name,
        "role": User.objects.get(email=request.session.get("user_email")).role,
        "status": User.objects.get(email=request.session.get("user_email")).status,
    }

    return render(request, 'EarlyWithdraw.html', {"user": user, "form_url": settings.MEDIA_URL})
