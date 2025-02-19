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

# Create your views here.
# Home view
def home(request):
    try:
        user = {
            "email": User.objects.get(email=request.session.get("user_email")).email,
            "name": User.objects.get(email=request.session.get("user_email")).name,
            "role": User.objects.get(email=request.session.get("user_email")).role,
            "status": User.objects.get(email=request.session.get("user_email")).status,
        }
    except:
        print("User not logged in or not created properly.")
        return redirect('/')

    return render(request, 'home.html', {"user": user})