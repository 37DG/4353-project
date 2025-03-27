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
            pdf_filename = f"{record.name.replace(' ', '_')}_PublicInfo_{record.date.strftime('%Y-%m-%d_%H_%M_%S')}.pdf"
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
                            f"PUBLIC_INFO_OPTIONA=Y", 
                            f"PUBLIC_INFO_NAME={name}", 
                            f"PUBLIC_INFO_ID={id}", 
                            f"PUBLIC_INFO_DATE={date}", 
                            f"PUBLIC_INFO_SIGNATURE={signature_path}"], cwd=latex_path)
        elif option == 'B':
            subprocess.run(["make", "buildPublicInfo", 
                            f"TEX_NAME=public_info.tex", 
                            f"PDFBASENAME={pdf_basename}", 
                            f"PUBLIC_INFO_OPTIONB=Y", 
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


    try:
        record = Early_withdrawal.objects.get(email=user['email'])

        if record.status == 'draft' or record.status =='returned':
            return render(request, 'EarlyWithdrawal.html', {"user": user, "form_url": settings.MEDIA_URL, "record": record})
        elif record.status == 'pending':
            return render(request, 'WaitForPending.html', {"user": user})
        elif record.status == 'approved':
            pdf_filename = f"{record.name.replace(' ', '_')}_EarlyWithdrawal_{record.date.strftime('%Y-%m-%d_%H_%M_%S')}.pdf"
            return render(request, 'EarlyWithdrawalApproved.html', {"user": user, "pdf_filename": pdf_filename})
    except Early_withdrawal.DoesNotExist:
        return render(request, 'EarlyWithdrawal.html', {"user": user, "form_url": settings.MEDIA_URL})
    

def saveEarlyWithdrawal(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("full_name")
        id = request.POST.get("id")
        step1_option = request.POST.get("step1_option")
        drop_course1 = request.POST.get("drop_course1")
        drop_course2 = request.POST.get("drop_course2")
        drop_course3 = request.POST.get("drop_course3")
        departure_date = request.POST.get("departure_date")
        step2_option = request.POST.get("step2_option")
        step3_option = request.POST.get("step3_option")
        return_date = request.POST.get("return_date")
        signature = request.FILES.get("signature")


        newname = name.replace(" ", "_")
        form = 'EarlyWithdrawal'
        if signature:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            file_extension = signature.name.split('.')[-1]
            signature_filename = f"{newname}_{form}.{file_extension}"
            file_path = os.path.join(settings.MEDIA_ROOT, signature_filename)

            # Delete the old file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)

            filename = fs.save(signature_filename, signature)

        Early_withdrawal.objects.update_or_create(
            email=email,
            defaults={
            'name':name,
            'ID' :id,
            'date':now(),
            'step1_option':step1_option,
            'drop_course1':drop_course1,
            'drop_course2':drop_course2,
            'drop_course3':drop_course3,
            'departure_date':departure_date,
            'step2_option':step2_option,
            'step3_option':step3_option,
            }
        )

        if return_date:
            record = Early_withdrawal.objects.get(email=email)
            record.return_date = return_date
            record.save()

        return redirect('http://localhost:8000/approvalsystem')
    
# Feature for user to submit the public information request
def submitEarlyWithdrawal(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("full_name")
        id = request.POST.get("id")
        step1_option = request.POST.get("step1_option")
        drop_course1 = request.POST.get("drop_course1")
        drop_course2 = request.POST.get("drop_course2")
        drop_course3 = request.POST.get("drop_course3")
        departure_date = request.POST.get("departure_date")
        step2_option = request.POST.get("step2_option")
        step3_option = request.POST.get("step3_option")
        return_date = request.POST.get("return_date")
        signature = request.FILES.get("signature")

        newname = name.replace(" ", "_")
        form = 'EarlyWithdrawal'
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

        Early_withdrawal.objects.update_or_create(
            email=email,
            defaults={
            'name':name,
            'ID' :id,
            'date':date,
            'step1_option':step1_option,
            'drop_course1':drop_course1,
            'drop_course2':drop_course2,
            'drop_course3':drop_course3,
            'departure_date':departure_date,
            'step2_option':step2_option,
            'step3_option':step3_option,
            'status': 'pending'
            }
        )

        if return_date:
            record = Early_withdrawal.objects.get(email=email)
            record.return_date = return_date
            record.save()

        # Run make file
        latex_path = os.path.abspath("Latex/")  # Path to Makefile
        pdf_basename = f"{newname}_{form}_{date.strftime('%Y-%m-%d_%H_%M_%S')}"


        make_command = [
            "make", "buildEarlyWithdrawal",
            f"TEX_NAME=early_withdrawal.tex",
            f"PDFBASENAME={pdf_basename}",
            f"EARLY_WITHDRAWAL_NAME={name}",
            f"EARLY_WITHDRAWAL_ID={id}",
            f"EARLY_WITHDRAWAL_DATE={date}",
            f"EARLY_WITHDRAWAL_SIGNATURE={signature_path}"
        ]

        # step1
        if step1_option == '1':
            make_command.append("STEP1_OPTION1=Y")
        elif step1_option == '2':
            make_command.append("STEP1_OPTION2=Y")
            if drop_course1:
                make_command.append(f"STEP1_DROP1={drop_course1}")
            if drop_course2:
                make_command.append(f"STEP1_DROP2={drop_course2}")
            if drop_course3:
                make_command.append(f"STEP1_DROP3={drop_course3}")
        elif step1_option == '3':
            make_command.append("STEP1_OPTION3=Y")

        # step2
        departure_parts = departure_date.split('-')
        if len(departure_parts) == 3:
            make_command.append(f"STEP2_MONTH={departure_parts[1]}")
            make_command.append(f"STEP2_DAY={departure_parts[2]}")
            make_command.append(f"STEP2_YEAR={departure_parts[0]}")

        if step2_option == '1':
            make_command.append("STEP2_OPTION1=Y")
        elif step2_option == '2':
            make_command.append("STEP2_OPTION2=Y")

        # step3
        if step3_option == '1':
            make_command.append("STEP3_OPTION1=Y")
            if return_date:
                make_command.append(f"STEP3_DATE={return_date}")
        elif step3_option == '2':
            make_command.append("STEP3_OPTION2=Y")


        subprocess.run(make_command, cwd=latex_path)

        return render(request, 'WaitForPending.html', {"user": {'name':name}})
    

def finishEarlyWithdrawal(request):
    record = Early_withdrawal.objects.get(email=request.session.get("user_email"))
    record.status = 'draft'
    record.note = ''
    record.save()

    return redirect('http://localhost:8000/approvalsystem')