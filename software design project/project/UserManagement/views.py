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

# The beginning page
def index(request):
    return render(request, 'index.html')

# After login, redirect to the dashboard page
def dashboard(request):
    return render(request, 'dashboard.html')

# Check user feature in the Dashboard page
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
    
# Administrator view
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
    paginator = Paginator(users, 2)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Retrieve username from session for personalized greeting
    name = request.session.get("name", "Admin")

    # Pass paginated users and username to the template
    return render(request, "Administrator.html", {"users": page_obj, "name": name})

# Basicuser view
def Basicuser(request):
    name = request.session.get("name", "User")  # Default to 'User' if not found
    return render(request, 'Basicuser.html', {"name": name})
    #return render(request, 'Basicuser.html')

# Create user feature from Administrator page
@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        role = data.get("role")
        status = data.get("status")

        if not name or not email or not role or status is None:
            return JsonResponse({"message": "All fields are required!"}, status=400)

        # Check if the user already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM user WHERE email=%s", [email])
            result = cursor.fetchone()
            if result[0] > 0:
                return JsonResponse({"message": "User with this email already exists!"}, status=400)

            # Insert the new user
            cursor.execute(
                "INSERT INTO user (name, email, role, status) VALUES (%s, %s, %s, %s)",
                [name, email, role, status]
            )
        return JsonResponse({"message": "User created successfully!"})

# Update user feature from Administrator page            
@csrf_exempt
def update_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")  # Email is required to identify the user
        name = data.get("name")  # Optional: new name
        role = data.get("role")  # Optional: new role
        status = data.get("status")  # Optional: new status

        if not email:
            return JsonResponse({"message": "Email is required to identify the user!"}, status=400)

        # Validate that at least one field to update is provided
        if not name and not role and not status:
            return JsonResponse({"message": "Provide at least one field to update!"}, status=400)

        with connection.cursor() as cursor:
            # Check if the user exists
            cursor.execute("SELECT COUNT(*) FROM user WHERE email=%s", [email])
            result = cursor.fetchone()

            if result[0] == 0:
                return JsonResponse({"message": "User not found!"}, status=404)

            # Build the update query dynamically
            update_fields = []
            params = []

            if name:
                update_fields.append("name=%s")
                params.append(name)
            if role:
                update_fields.append("role=%s")
                params.append(role)
            if status:
                update_fields.append("status=%s")
                params.append(status)

            # Add WHERE clause for the email
            query = f"UPDATE user SET {', '.join(update_fields)} WHERE email=%s"
            params.append(email)

            # Execute the update query
            cursor.execute(query, params)

        return JsonResponse({"message": "User updated successfully!"})

# Delete user feature from Administrator page    
@csrf_exempt
def delete_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return JsonResponse({"message": "Name and email are required!"}, status=400)

        with connection.cursor() as cursor:
            # Check if the user exists
            cursor.execute("SELECT role FROM user WHERE name=%s AND email=%s", [name, email])
            result = cursor.fetchone()

            if not result:
                return JsonResponse({"message": "User not found!"}, status=404)

            role = result[0]

            # Prevent deleting administrators
            if role == "Administrator":
                return JsonResponse({"message": "You cannot delete an Administrator!"}, status=403)

            # Delete the user
            cursor.execute("DELETE FROM user WHERE name=%s AND email=%s", [name, email])
        return JsonResponse({"message": "User deleted successfully!"})
