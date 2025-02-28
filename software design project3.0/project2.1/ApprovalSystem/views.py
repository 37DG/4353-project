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
from django.conf import settings

import os
import subprocess
from django.http import FileResponse

def RequestMenu(request):
    user = {
        "email": User.objects.get(email=request.session.get("user_email")).email,
        "name": User.objects.get(email=request.session.get("user_email")).name,
        "role": User.objects.get(email=request.session.get("user_email")).role,
        "status": User.objects.get(email=request.session.get("user_email")).status,
    }

    return render(request, 'RequestMenu.html', {"user": user})


def PublicInformation(request):
    user = {
        "email": User.objects.get(email=request.session.get("user_email")).email,
        "name": User.objects.get(email=request.session.get("user_email")).name,
        "role": User.objects.get(email=request.session.get("user_email")).role,
        "status": User.objects.get(email=request.session.get("user_email")).status,
    }

    return render(request, 'PublicInformation.html', {"user": user, "form_url": settings.MEDIA_URL})




















def EarlyWithdraw(request):
    user = {
        "email": User.objects.get(email=request.session.get("user_email")).email,
        "name": User.objects.get(email=request.session.get("user_email")).name,
        "role": User.objects.get(email=request.session.get("user_email")).role,
        "status": User.objects.get(email=request.session.get("user_email")).status,
    }

    return render(request, 'EarlyWithdraw.html', {"user": user, "form_url": settings.MEDIA_URL})