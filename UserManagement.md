Catalog:
1. models.py
   1.1 class User
       // This module defines the User model for the application.
       // It utilizes Django’s ORM (django.db.models) to map Python class objects to relational database tables.
       attributes:
           email: char(255), primary key
           name: char(255)
           role: char(45)
           status: char(1)  // '0' for deactivated, '1' for active

2. views.py
    2.0 imported packages:
    2.1 def index()
        // input: http request
        // return index.html 
        // index.html displays the Microsoft login button.
        // The Microsoft login button redirects the user to (2.2) microsoft_login().
    2.2 def microsoft_login()
        // input: http request
        // return redirection to Microsoft login page through Microsoft Azure
    2.3 def logout_view()
        // input: http request
        // return redirection to Microsoft logout page through Microsoft Azure
    2.4 def login_view()
        // input: http request
        // The login_view function handles the Microsoft OAuth authentication callback.
        // It retrieves the authentication code from the request, exchanges it for an access token,
        // and fetches user details from the Microsoft Graph API.
        // Examine the database:
            // 1. If the user does not exist in the database, create a new user and store related information in the database.
                  -- If no previous user existed in the database, the user is automatically set to the role Administrator.
            // 2. If the user exists in the database, retrieve the user imformation from the database.
        // Status:
            // 1. If the user status is '0', return redirection to (2.6) Deactivated_user().
            // 2. If the user status is '1', return redirection to (???) home().
    2.5 def profile()
        // input: http request
        // Confirm the role of the user through the database.
        // If the user is with the role Administrator, return redirection to (???) Administrator().
        // If the user is with the role Basicuser, return redirection to (???) Basicuser().
   2.6 def Deactivated_user()
       // input http request
       // return
   2.7 def Administrator()
   2.8 def Basicuser()
   2.9 def changeUsername()
   2.10 def create_user()
   2.11 update_user()
   2.12 delete_user()
   
   2.100 def home() 
   

