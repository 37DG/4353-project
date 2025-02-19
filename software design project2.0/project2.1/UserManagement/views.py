from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
import msal
import requests
import base64
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from UserManagement.models import User
from django.conf import settings

# The beginning page
def index(request):
    return render(request, 'index.html')

def microsoft_login(request):
    """Redirects the user to Microsoft OAuth login page."""
    auth_url = (
        f"https://login.microsoftonline.com/{settings.MICROSOFT_AUTH['TENANT_ID']}/oauth2/v2.0/authorize"
        f"?client_id={settings.MICROSOFT_AUTH['CLIENT_ID']}"
        f"&response_type=code"
        f"&redirect_uri={settings.MICROSOFT_AUTH['REDIRECT_URI']}"
        f"&response_mode=query"
        f"&scope=User.Read"
        f"&state=12345"
    )
    return redirect(auth_url)

def logout_view(request):
    """Logs out the user, clears session, and redirects them to the Microsoft logout page."""
    
    # Clear the session
    request.session.flush()

    # Redirect to Microsoft logout endpoint
    microsoft_logout_url = (
        f"https://login.microsoftonline.com/{settings.MICROSOFT_AUTH['TENANT_ID']}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={settings.MICROSOFT_AUTH['LOGOUT_REDIRECT_URI']}"
    )

    return redirect(microsoft_logout_url)

def login_view(request):
    """Handle Microsoft OAuth callback, create user if needed, and redirect based on role."""
    if "code" in request.GET:
        auth_code = request.GET["code"]

        msal_app = msal.ConfidentialClientApplication(
            settings.MICROSOFT_AUTH["CLIENT_ID"],
            client_credential=settings.MICROSOFT_AUTH["CLIENT_SECRET"],
            authority=settings.MICROSOFT_AUTH["AUTHORITY"],
        )

        token_response = msal_app.acquire_token_by_authorization_code(
            auth_code,
            scopes=["User.Read"],
            redirect_uri=settings.MICROSOFT_AUTH["REDIRECT_URI"],
        )

        if "access_token" in token_response:
            access_token = token_response["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Fetch user information from Microsoft Graph API
            user_info = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()

            raw_name = user_info.get("displayName", "Unknown User")  # Ex: "Doe, John"
            user_email = user_info.get("mail", "No email available")
            user_id = user_info.get("id", "No ID available")

            # Fix name formatting from "Lastname, Firstname" to "Firstname Lastname"
            if "," in raw_name:
                last_name, first_name = raw_name.split(", ")
                user_name = f"{first_name} {last_name}"
            else:
                user_name = raw_name  # If format is already correct, keep it

            #request.session["name"] = user_name
            print(f"User logged in: {user_name} ({user_email}), ID: {user_id}")

            # Default role and status
            role = "Basicuser"
            status = '1'  # 1 = Active, 0 = Inactive


            sel_user = get_object_or_404(User, email=user_email)
            role = sel_user.role
            status = sel_user.status


            # with connection.cursor() as cursor:
            #     # Check if the user already exists
            #     cursor.execute("SELECT role, status FROM usermanagement_user WHERE email=%s", [user_email])
            #     existing_user = cursor.fetchone()

            #     if existing_user:
            #         role, status = existing_user  # Retrieve existing role and status
            #     else:
            #         # If no users exist in the system, make the first user an Administrator
            #         cursor.execute("SELECT COUNT(*) FROM usermanagement_user")
            #         user_count = cursor.fetchone()[0]

            #         if user_count == 0:
            #             role = "Administrator"

            #         # Insert new user into the database
            #         cursor.execute(
            #             "INSERT INTO usermanagement_user (name, email, role, status) VALUES (%s, %s, %s, %s)",
            #             [user_name, user_email, role, status]
            #         )
            #         print("New user created in the database.")

            # Store user info in session
            request.session["user_email"] = user_email
            request.session["user_name"] = user_name
            request.session["user_id"] = user_id
            request.session["user_role"] = role
            request.session["user_status"] = status

            # Redirect user based on role
            if status == '0':
                return redirect('/Deactivated_User/?name=%s'%user_name)
            
            return redirect('/home')

        # If token response fails, log the error
        print("DEBUG: Microsoft OAuth token response failed", token_response)
        return JsonResponse({"status": "error", "message": "Failed to retrieve access token"}, status=401)

    return JsonResponse({"status": "error", "message": "Authentication failed"}, status=401)


def profile(request):
    name = User.objects.get(email=request.session.get("user_email")).name
    role = User.objects.get(email=request.session.get("user_email")).role

    if role == "Administrator":
        return redirect("/Administrator/?name=%s"%name)
    else:
        return redirect("/Basicuser/?name=%s"%name)

# Deactivated user view
def Deactivated_User(request):
    name = request.GET.get("name", "User")  # Default to 'User' if not found
    return render(request, 'Deactivated_User.html', {"name": name})

# Administrator view
def Administrator(request):
    # Query all user records
    users = User.objects.all().order_by("name")

    # Paginate the data (5 records per page)
    paginator = Paginator(users, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Retrieve username from session for personalized greeting
    name = request.GET.get("name", "Admin")

    # Pass paginated users and username to the template
    return render(request, "Administrator.html", {"users": page_obj, "name": name})

# Basicuser view
def Basicuser(request):
    name = request.GET.get("name", "User")  # Default to 'User' if not found
    return render(request, 'Basicuser.html', {"name": name})

# Basicuer change user name
@csrf_exempt
def changeUsername(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")

        if not name:
            return JsonResponse({"message": "Name is required!"}, status=400)
        
        user_email = request.session.get("user_email")
        if not user_email:
            return JsonResponse({"message": "User not authenticated!"}, status=401)
        
        user = User.objects.get(email=request.session.get("user_email"))
        user.name = name
        user.save()

        request.session["user_name"] = name

        return JsonResponse({"message": "Name updated successfully!"})

# Create user feature from Administrator page
@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        role = data.get("role")
        status = data.get("status")

        if not name or not email or not role or not status:
            return JsonResponse({"message": "All fields are required!"}, status=400)

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "User with this email already exists!"}, status=400)

        # Create and save user using ORM
        User.objects.create(email=email, name=name, role=role, status=status)
            
        return JsonResponse({"message": "User created successfully!"}, status=201)

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

        # Check if the user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found!"}, status=404)

        # Update fields if they are provided
        if name:
            user.name = name
            request.session["user_name"] = name
        if role:
            user.role = role
            request.session["user_role"] = role
        if status:
            user.status = status
            request.session["user_status"] = status

        # Save the changes
        user.save()

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

        # Check if the user exists
        try:
            user = User.objects.get(email=email, name=name)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found!"}, status=404)
        
        # Prevent deleting administrators
        if user.role == "Administrator":
            return JsonResponse({"message": "You cannot delete an Administrator!"}, status=403)
        
        # Delete the user
        user.delete()

        return JsonResponse({"message": "User deleted successfully!"})


