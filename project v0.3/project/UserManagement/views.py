from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
import msal
import requests
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import User
from ApprovalSystem.models import Public_info, Early_withdrawal
from django.conf import settings

import os
import subprocess
from django.http import FileResponse

#from rest_framework import viewsets
#from .serializers import UserSerializer

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

            try:
                sel_user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                if len(User.objects.all()) == 0:
                    sel_user = User.objects.create(email=user_email, name=user_name, role="Administrator", status="1")
                else:
                    print(f"New user {user_email} created")
                    sel_user = User.objects.create(email=user_email, name=user_name, role="Basicuser", status="1")

            role = sel_user.role
            status = sel_user.status
            user_name = sel_user.name

            # call flask to add user
            requests.post(
                "http://flask_web:5002/add_user",
                json={"email": user_email,
                      "name": user_name,
                      "role":role,
                      "account_status":status},
                headers={"Content-Type": "application/json"}
            )

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
        
        # Update the user name in the database and session
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

        # call flask to add user
        flask_role = role
        if role == "Basicuser":
            flask_role = "basicUser"
        else:
            flask_role = "admin"
        
        flask_account_status = True
        if status == '0':
            flask_account_status = False

        requests.post("http://flask_web:5002/add_user",
            json={"email": email,
                  "name": name,
                  "role":flask_role,
                  "account_status":flask_account_status},
            headers={"Content-Type": "application/json"}
        )
            
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

        # call flask to update user
        flask_name = User.objects.get(email=email).name
        if name:
            flask_name = name
        
        flask_role = User.objects.get(email=email).role
        if role:
            flask_role = role
        if flask_role == "Basicuser":
            flask_role = "basicUser"
        else:
            flask_role = "admin"

        flask_account_status = User.objects.get(email=email).status
        if status:
            flask_account_status = status
        if flask_account_status == '1':
            flask_account_status = "True"
        else:
            flask_account_status = "False"

        requests.post("http://flask_web:5002/update_user",
            json={
                "users": [{
                    "email": email,
                    "name": flask_name,
                    "role": flask_role,
                    "account_status": flask_account_status}]},
            headers={"Content-Type": "application/json"}
        )

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

        # call flask to delete user
        requests.post("http://flask_web:5002/delete_user",
            json={"email": email},
            headers={"Content-Type": "application/json"}
        )

        return JsonResponse({"message": "User deleted successfully!"})


# PublicInformation form Pending
def PublicInformationPending(request):
    # Query all records from Public_info table
    records = Public_info.objects.filter(status='Pending')

    # Paginate the data (5 records per page)
    paginator = Paginator(records, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Retrieve username from session for personalized greeting
    name = request.session.get("user_name", "User")

    # Pass paginated users and username to the template
    return render(request, "PublicInformationPending.html", {"records": page_obj, "name": name})


# EarlyWithdraw form Pending
def EarlyWithdrawalPending(request):
    # Query all records from Public_info table
    records = Early_withdrawal.objects.filter(status='Pending')

    # Paginate the data (5 records per page)
    paginator = Paginator(records, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Retrieve username from session for personalized greeting
    name = request.session.get("user_name", "User")

    # Pass paginated users and username to the template
    return render(request, "EarlyWithdrawalPending.html", {"records": page_obj, "name": name})

# View Pending form details
def ViewPending(request):
    name = request.session.get("user_name", "User")
    user_name = request.GET.get("name").replace(" ", "_")
    user_form = request.GET.get("form")
    user_date = request.GET.get("date")
    user_email = request.GET.get("email")

    pdf_filename = f"{user_name}_{user_form}_{user_date}.pdf"

    return render(request, 'ViewPending.html', {"name": name, "pdf_filename": pdf_filename, "form": user_form, "email": user_email})

# Return pending form
def ReturnPending(request):
    form = request.GET.get("form")
    email = request.GET.get("email")
    note = request.GET.get("note")

    if form == 'PublicInfo':
        table = Public_info
        redirection = '/PublicInformationPending/'
    elif form == 'EarlyWithdrawal':
        table = Early_withdrawal
        redirection = '/EarlyWithdrawalPending/'

    record = table.objects.get(email=email)
    record.status = 'returned'
    record.note = note
    record.save()

    return redirect(redirection)


# Approve Pending form
def ApprovePending(request):
    form = request.GET.get("form")
    email = request.GET.get("email")

    if form == 'PublicInfo':
        table = Public_info
        redirection = '/PublicInformationPending/'
    elif form == 'EarlyWithdrawal':
        table = Early_withdrawal
        redirection = '/EarlyWithdrawalPending/'

    record = table.objects.get(email=email)
    record.status = 'approved'
    record.save()

    return redirect(redirection)

#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializerz


######################################################################################
#Graduate Petition Pending
def GraduatePetitionPending(request):
    # Retrieve username from session for personalized greeting
    name = request.session.get("user_name", "User")
    
    response = requests.post(
        "http://flask_web:5002/get_forms_by_name",
        json={"formName": "graduate student petition form"},
        headers={"Content-Type": "application/json"}
    )
    forms = []
    if response.status_code == 200:
        forms = response.json().get("forms", [])

    return render(request, "GraduatePetitionPending.html", {"forms": forms, "name": name})

# Undergraduate Transfer Pending
def UndergraduateTransferPending(request):
    # Retrieve username from session for personalized greeting
    name = request.session.get("user_name", "User")
    
    response = requests.post(
        "http://flask_web:5002/get_forms_by_name",
        json={"formName": "undergraduate transfer form"},
        headers={"Content-Type": "application/json"}
    )
    forms = []
    if response.status_code == 200:
        forms = response.json().get("forms", [])

    return render(request, "UndergraduateTransferPending.html", {"forms": forms, "name": name})


# View pending for tow new forms
def newViewPending(request):
    name = request.session.get("user_name", "User")
    user_form = request.GET.get("form")
    user_email = request.GET.get("email")

    pdf_filename = f"{user_email.lower().strip().replace('@', '_')}_{user_form}.pdf"

    #return HttpResponse(f"{name} | {user_form} | {user_email} | {pdf_filename}")
    return render(request, 'newViewPending.html', {"name": name, "pdf_filename": pdf_filename, "form": user_form, "email": user_email})

# new Return pending form
def newReturnPending(request):
    form = request.GET.get("form")
    email = request.GET.get("email")
    note = request.GET.get("note", "")

    form_name = ""
    if form == "GraduatePetition":
        form_name = "graduate student petition form"
    elif form == "UndergraduateTransfer":
        form_name = "undergraduate transfer form"

    # Step 1: Get form info from Flask
    try:
        id_response = requests.post(
            "http://flask_web:5002/get_form_info",
            json={"email": email, "formName": form_name},
            headers={"Content-Type": "application/json"}
        )
        if id_response.status_code != 200:
            return HttpResponse(f"Error fetching form ID: {id_response.text}", status=500)

        form_id = id_response.json().get("formId")
        if not form_id:
            return HttpResponse("Form ID not found.", status=404)
        
        #return HttpResponse(f"Form ID fetched: {form_id}")
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error connecting to Flask: {str(e)}", status=500)
    
    # Step 2: Send return request to Flask
    try:
        return_response = requests.post(
            "http://flask_web:5002/return-form",
            json={
                "returnedFormId": form_id,
                "comment": note
            },
            headers={"Content-Type": "application/json"}
        )

        if return_response.status_code == 200:
            # Redirect back to pending list
            if form == "GraduatePetition":
                return redirect("/GraduatePetitionPending/")
            elif form == "UndergraduateTransfer":
                return redirect("/UndergraduateTransferPending/")
            else:
                return redirect("/")
        else:
            return HttpResponse(f"Error returning form: {return_response.text}", status=500)

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error connecting to Flask (return-form): {str(e)}", status=500)


# new Approve Pending form
def newApprovePending(request):
    name = request.session.get("user_name", "User")
    form = request.GET.get("form")
    email = request.GET.get("email")

    form_name = ""
    if form == "GraduatePetition":
        form_name = "graduate student petition form"
    elif form == "UndergraduateTransfer":
        form_name = "undergraduate transfer form"

    # Step 1: Get form info from Flask
    try:
        id_response = requests.post(
            "http://flask_web:5002/get_form_info",
            json={"email": email, "formName": form_name},
            headers={"Content-Type": "application/json"}
        )
        if id_response.status_code != 200:
            return HttpResponse(f"Error fetching form ID: {id_response.text}", status=500)

        form_id = id_response.json().get("formId")
        if not form_id:
            return HttpResponse("Form ID not found.", status=404)
        
        #return HttpResponse(f"Form ID fetched: {form_id}")
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error connecting to Flask: {str(e)}", status=500)
    
    # Step 2: Send approve request to Flask
    try:
        return_response = requests.post(
            "http://flask_web:5002/approve-deny-form",
            json={
                "formId": form_id,
                "status": "approved"
            },
            headers={"Content-Type": "application/json"})

        if return_response.status_code == 200:
            # Redirect back to pending list
            if form == "GraduatePetition":
                return redirect("/GraduatePetitionPending/")
            elif form == "UndergraduateTransfer":
                return redirect("/UndergraduateTransferPending/")
            else:
                return redirect("/")
        else:
            return HttpResponse(f"Error returning form: {return_response.text}", status=500)

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error connecting to Flask (return-form): {str(e)}", status=500)

