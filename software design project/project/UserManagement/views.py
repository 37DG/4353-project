from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.db import connection

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
User = get_user_model()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def check_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("username")
        email = data.get("email")

        with connection.cursor() as cursor:
            cursor.execute("SELECT role, status FROM user WHERE name=%s AND email=%s", [name, email])
            result = cursor.fetchone()  # Get the result


        if result:
            role, status = result  # Extract role and status
            # selfCheck
            print(f"DEBUG: Found user with role={role}, status={status}")

            if status == '0':
                return JsonResponse({"message": "You are deactivated"})
            
            request.session["name"] = name  # Store username in session

            if role == "Administrator":
                return JsonResponse({"redirect": "/Administrator"})

            if role == "Basicuser":
                return JsonResponse({"redirect": "/Basicuser"})

        # If no matching user is found
        return JsonResponse({"message": "You are not our user"})
    

def Administrator(request):
    # Query all user records
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, email, role, status FROM user")
        users_data = cursor.fetchall()

    # Convert raw data into a dictionary
    users = [
        {"name": row[0], "email": row[1], "role": row[2], "status": row[3]}
        for index, row in enumerate(users_data)
    ]

    # Paginate the data (5 records per page)
    paginator = Paginator(users, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Retrieve username from session for personalized greeting
    name = request.session.get("name", "Admin")

    # Pass paginated users and username to the template
    return render(request, "Administrator.html", {"users": page_obj, "name": name})

def Basicuser(request):
    name = request.session.get("name", "User")  # Default to 'User' if not found
    return render(request, 'Basicuser.html', {"name": name})
    #return render(request, 'Basicuser.html')