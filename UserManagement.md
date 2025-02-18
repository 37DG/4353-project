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
        // index.html displays the Microsoft login button
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
            // 1. If the user exists in the database, retrieve the user imformation from the database.
            // 2. 
   
4. urls.py
5. views.py
