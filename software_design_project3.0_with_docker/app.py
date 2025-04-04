import requests
from flask import Flask, redirect, request, session, url_for, render_template,g,jsonify, Response
import app_config
import psycopg2
from urllib.parse import urlencode
import os
import subprocess
import base64
import io
import logging
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(app_config)
app.secret_key = "your_secret_key_here"
SAVE_DIR = "saved_tex_files"
os.makedirs(SAVE_DIR, exist_ok=True)


createDatabase = """
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255),
    account_status BOOLEAN
);

CREATE TABLE IF NOT EXISTS forms (
    form_id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    form_name VARCHAR(255),
    form_content TEXT,
    status VARCHAR(255),
    user_signature BYTEA,
    approver_signature BYTEA,
    approver_comment VARCHAR(255),
    CONSTRAINT unique_email_form_name UNIQUE (email, form_name)
);

INSERT INTO users (email, name, role, account_status)
VALUES 
    (LOWER('tbnguy36@CougarNet.UH.EDU'), 'Nguyen, Binh', 'admin', TRUE),
    (LOWER('fmmancil@cougarnet.uh.edu'), 'Mancilla, Fernando', 'admin', TRUE),
    (LOWER('rlpham3@cougarnet.uh.edu'), 'Pham, Ryan', 'admin', TRUE),
    (LOWER('john.doe@CougarNet.UH.EDU'), 'John Doe', 'undergraduate-student', TRUE),
    (LOWER('jane.smith@CougarNet.UH.EDU'), 'Jane Smith', 'undergraduate-student', FALSE),
    (LOWER('alice.johnson@CougarNet.UH.EDU'), 'Alice Johnson', 'graduate-student', TRUE),
    (LOWER('bob.williams@CougarNet.UH.EDU'), 'Bob Williams', 'graduate-student', FALSE)
ON CONFLICT (email) DO NOTHING;

"""


def save_signature(base64_str):
    image_data = base64.b64decode(base64_str.split(",")[1])
    with open("signature.png", "wb") as f:
        f.write(image_data)

def get_user_by_email(email):
    if not email:
        return None
    g.db_cursor.execute("SELECT email, name, role, account_status FROM users WHERE email = %s", (email,))
    user = g.db_cursor.fetchone()

    if user:
        return {
            "email": user[0],
            "name": user[1],
            "role": user[2],
            "account_status": user[3],
        }
    return None 

@app.before_request
def before_request():
    g.db_conn = psycopg2.connect(
        host=app_config.DB_HOST,
        port=app_config.DB_PORT,
        dbname=app_config.DB_NAME,
        user=app_config.DB_USER,
        password=app_config.DB_PASSWORD
    )
    g.db_cursor = g.db_conn.cursor()
    g.db_cursor.execute(createDatabase)
    g.db_conn.commit()
    print("Database connected")

@app.after_request
def after_request(response):
    g.db_cursor.close()
    g.db_conn.close()
    return response

def getTable(tableName):
    query = f"SELECT * FROM {tableName};"
    g.db_cursor.execute(query)
    forms = g.db_cursor.fetchall()
    col_names = [desc[0] for desc in g.db_cursor.description]
    form_dict = {form[0]: dict(zip(col_names,form)) for form in forms}
    return form_dict

def getUserInfo(email):
    query = f"SELECT * FROM users WHERE email = %s"
    g.db_cursor.execute(query,(email,))
    user = g.db_cursor.fetchone()

    if user:
        col_names = [desc[0] for desc in g.db_cursor.description]
        return dict(zip(col_names,user))
    else:
        return None
def getFormByEmailAndName(email, form_name):
    query = """
    SELECT * FROM forms WHERE email = %s AND form_name = %s;
    """
    g.db_cursor.execute(query, (email, form_name))
    form = g.db_cursor.fetchone()
    
    if form:
        col_names = [desc[0] for desc in g.db_cursor.description]
        return dict(zip(col_names, form))
    else:
        return None 


def add_or_update_form(email, form_name, form_content, status, user_signature, approver_signature, approver_comment):

    query = """
    INSERT INTO forms (email, form_name, form_content, status, user_signature, approver_signature, approver_comment)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (email, form_name) 
    DO UPDATE SET 
        form_content = EXCLUDED.form_content,
        status = EXCLUDED.status,
        user_signature = EXCLUDED.user_signature,
        approver_signature = EXCLUDED.approver_signature,
        approver_comment = EXCLUDED.approver_comment;
    """
    try:
        g.db_cursor.execute(query, (email, form_name, form_content, status, user_signature, approver_signature, approver_comment))
        g.db_conn.commit()
        print("Form added or updated successfully.")
    except Exception as e:
        g.db_conn.rollback()
        print("Error:", e)

# Microsoft Login URL
@app.route("/login")
def login():
    auth_url = f"{app_config.AUTHORITY}/oauth2/v2.0/authorize?"
    auth_params = {
        'client_id': app_config.CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': url_for('auth_response', _external=True),
        'scope': ' '.join(app_config.SCOPE),
        'state': '12345'
    }
    return redirect(auth_url + urlencode(auth_params))

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json 
    email = data.get("email").lower()
    name = data.get("name")
    role = data.get("role", "undergraduate-student")
    account_status = data.get("account_status", True) 
    user = getUserInfo(email)
    if user:
        if not user.get("account_status"):
            return jsonify({"error": "User is deactivated."}), 401
    if not user:
        g.db_cursor.execute(
            "INSERT INTO users (email, name, role, account_status) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING",
            (email, name, role, account_status),
        )
        g.db_conn.commit()

    return jsonify({"message": "User added successfully"}), 201


@app.route("/update_user", methods=["POST"])
def update_user():
    updated_users = request.json.get('users') 
    for user_data in updated_users:
        email = user_data.get("email").lower()
        new_name = user_data.get("name")
        new_role = user_data.get("role")
        new_status = user_data.get("account_status")
        if user_data.get("account_status") == "True":
            new_status = True
        else:
            new_status = False
        query = """
            UPDATE users 
            SET name = %s, role = %s, account_status = %s 
            WHERE email = %s
        """
        g.db_cursor.execute(query, (new_name, new_role, new_status, email))
        g.db_conn.commit()

    return {"message": "User information updated successfully"}, 200

@app.route("/delete_user", methods=["POST"])
def delete_user():

    data = request.json
    email = data.get("email").lower()
    user = getUserInfo(email)
    if not user:
        return {"message": "User not found"}, 404

    g.db_cursor.execute("DELETE FROM users WHERE email = %s", (email,))
    g.db_conn.commit()
    return {"message": "User deleted"}, 200


# Authentication Callback
@app.route(app_config.REDIRECT_PATH)
def auth_response():
    code = request.args.get('code')
    if not code:
        return "Error: No authorization code received", 400

    token_url = f"{app_config.AUTHORITY}/oauth2/v2.0/token"
    token_data = {
        'client_id': app_config.CLIENT_ID,
        'client_secret': app_config.CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('auth_response', _external=True),
    }

    token_response = requests.post(token_url, data=token_data)
    token_info = token_response.json()
    access_token = token_info.get('access_token')

    if access_token:
        session['access_token'] = access_token

        # Fetch user info from Microsoft Graph API
        graph_url = 'https://graph.microsoft.com/v1.0/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info = requests.get(graph_url, headers=headers).json()

        session['user'] = {
            'name': user_info.get('displayName').lower(),
            'email': user_info.get('userPrincipalName').lower(),
        }
        url = f"http://localhost:{app_config.PORT}/add_user"
        data = session['user']
        res = requests.post(url,json=data)
        return redirect(url_for('index'))
    
    return "Error: Unable to retrieve token", 400

# Home Page
@app.route("/")
def index():
    user = session.get("user") 
    userinfo = None
    if user:
        userinfo = get_user_by_email(user['email'])
    forms = getTable("forms")
    return render_template("index.html", user=userinfo,forms = forms)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri=" + url_for('index', _external=True))

@app.route("/admin")
def admin_dash():
    user = session.get("user")
    if not user:
        return "Forbidden", 403
    currUser = getUserInfo(user['email'])
    if (currUser.get('role').lower() != "admin"):
        return "Forbidden", 403
    users = getTable("users")
    forms = getTable("forms")
    if (forms):
        for formId,formDetails in forms.items():
            if formDetails.get("approver_signature"):
                
                formDetails["approver_signature"] = base64.b64encode(formDetails["approver_signature"]).decode('utf-8')
    return render_template("admin.html",users=users,forms=forms,currUser=currUser)

@app.route("/reactivate", methods=["POST"])
def reactivate_account():
    try:

        data = request.get_json()  
        email = data.get('email')

        if not email:
            return jsonify({"success": False, "message": "No email provided"}), 400
        
        g.db_cursor.execute("UPDATE users SET account_status = %s WHERE email = %s", (True, email))
        g.db_cursor.connection.commit() 
        
        return jsonify({"success": True, "message": "Account reactivated successfully"})
    
    except Exception as e:
        print(f"Error reactivating account: {e}")
        return jsonify({"success": False, "message": "An error occurred while reactivating the account"}), 500

@app.route("/graduate-student-petition-form")
def handleGraduateStudentPetitionForm():
    user = session.get("user") 
    userinfo = None
    if user:
        userInfo = getUserInfo(user['email'])
    userName = user['name'].split(",")
    filledForm = getFormByEmailAndName(user.get("email"),"graduate student petition form")
    filledFormStatus = None
    if filledForm:
        filledFormStatus = filledForm.get("status")

    return render_template("forms/graduate_student_petition_form.html",userName=userName,currUser=userInfo,filledFormStatus=filledFormStatus)

@app.route("/return-form",methods=["POST"])
def returnForm():
    data = request.get_json()
    returnedFormId = int(data.get("returnedFormId"))
    comment = data.get("comment")
    status = "returned"
    forms = getTable("forms")
    returnedFormDetails = forms.get(returnedFormId)
    add_or_update_form(returnedFormDetails["email"], returnedFormDetails["form_name"],returnedFormDetails["form_content"],status,returnedFormDetails["user_signature"],returnedFormDetails["approver_signature"],comment)
    return jsonify({"message": "successfully return form"})

@app.route("/undergraduate-transfer-form")
def undergraduateTransferForm():
    user = session.get("user") 
    userinfo = None
    if user:
        userinfo = getUserInfo(user.get("email"))
    userName = user.get('name').split(',')
    filledForm = getFormByEmailAndName(user.get("email"),"undergraduate transfer form")
    filledFormStatus = None
    if filledForm:
        filledFormStatus = filledForm.get("status")
    return render_template("forms/undergraduate_transfer_form.html",userName=userName,currUser=userinfo,filledFormStatus=filledFormStatus)

@app.route('/approve-deny-form', methods=['POST'])
def approve_deny_form():
    try:
        #user = session.get("user")
        #if not user or "email" not in user:
        #    print("yes")
        #    return jsonify({"error": "User not authenticated"}), 401
        data = request.get_json()
        formId = data.get("formId")
        approverSignatureBase64 = data.get("approverSignatureBase64")
        status = data.get("status")
        approver_signature_binary = None
        if approverSignatureBase64:
            try:
                approver_signature_binary = base64.b64decode(approverSignatureBase64.split(",")[1])
            except (IndexError, ValueError):
                return jsonify({"error": "Invalid signature format"}), 400

        query = """
        UPDATE forms
        SET status = %s, approver_signature = %s
        WHERE form_id = %s;
        """
        data = (status,approver_signature_binary,formId)
        g.db_cursor.execute(query,data)
        g.db_conn.commit()
        return jsonify({"message": "approved form"})

    except Exception as e:
        return jsonify({"Error message": "Error approved form"})
    

@app.route('/update-latex', methods=['POST'])
def update_latex():
    try:
        user = session.get("user")
        if not user or "email" not in user:
            return jsonify({"error": "User not authenticated"}), 401

        data = request.get_json()
        latex_content = data.get("content")
        signature_base64 = data.get("signature")
        form_name = data.get("formName")

        if latex_content is None:
            return jsonify({"error": "Missing LaTeX content"}), 400

        # Convert signature from Base64 to binary
        signature_binary = None
        if signature_base64:
            try:
                signature_binary = base64.b64decode(signature_base64.split(",")[1])
            except (IndexError, ValueError):
                return jsonify({"error": "Invalid signature format"}), 400


        query = '''
        INSERT INTO forms (email, form_name, form_content, status, user_signature, approver_signature,approver_comment)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (email, form_name) 
        DO UPDATE SET 
            status = EXCLUDED.status,
            form_content = EXCLUDED.form_content,
            user_signature = EXCLUDED.user_signature;
        '''
        user_email = user["email"].lower().strip()
        status = "pending"
        approver_signature = None
        approver_comment = ""
        data = (user_email, form_name, latex_content, status, signature_binary,approver_signature,approver_comment)
        g.db_cursor.execute(query, data)

        g.db_conn.commit()
        return jsonify({"message": "LaTeX and signature updated"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/show_pdf", methods=["POST"])
def show_pdf():
    data = request.get_json()

    if not data or "formId" not in data:
        return jsonify({"error": "Missing LaTeX content"}), 400

    formId = data["formId"]
    userEmail = data["userEmail"]

    query_latex = """
    SELECT form_content, user_signature
    FROM forms
    WHERE form_id = %s
    """
    g.db_cursor.execute(query_latex, (formId,))
    result = g.db_cursor.fetchone()

    if not result or not result[0]:
        return jsonify({"error": "No LaTeX content found for this user"}), 404

    full_latex = result[0] 
    signature_image_data = result[1]

    file_name = f"{userEmail}_petition"

    with open(f"{file_name}.tex", "w", encoding="utf-8") as f:
        f.write(full_latex)


    if signature_image_data:
        with open("signature.png", "wb") as f:
            f.write(signature_image_data)
        print("Signature image saved as signature.png")


    process = subprocess.run(["make",f"TEX_FILE={file_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.returncode != 0:
        print("Make failed with error:", process.stderr.decode())
        return jsonify({"error": process.stderr.decode()}), 500

    pdf_output = io.BytesIO()
    with open(f"{file_name}.pdf", "rb") as f:
        pdf_output.write(f.read())

    pdf_output.seek(0)
    process = subprocess.run(["make","clean",f"TEX_FILE={file_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return Response(pdf_output, mimetype="application/pdf")

@app.route("/get_form_info", methods=["POST"])
def get_form_info():
    data = request.get_json()

    if not data or "email" not in data or "formName" not in data:
        return jsonify({"error": "Missing email or formName"}), 400

    email = data["email"].strip().lower()
    form_name = data["formName"].strip().lower()

    query = """
    SELECT form_id, status, approver_comment
    FROM forms
    WHERE LOWER(email) = %s AND LOWER(form_name) = %s
    LIMIT 1
    """
    g.db_cursor.execute(query, (email, form_name))
    result = g.db_cursor.fetchone()

    if not result:
        return jsonify({"status": "not_found"}), 220

    return jsonify({"formId": result[0], "status": result[1], "comment": result[2]})

@app.route("/set-user-session", methods=["POST"])
def set_user_session():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Missing username or email"}), 400

    session["user"] = {
        "name": username,
        "email": email
    }

    return jsonify({"message": "Session set successfully"})

@app.route("/get_forms_by_name", methods=["POST"])
def get_forms_by_name():
    data = request.get_json()

    if not data or "formName" not in data:
        return jsonify({"error": "Missing formName"}), 400

    form_name = data["formName"].strip().lower()

    query = """
    SELECT form_id, email, form_name, status
    FROM forms
    WHERE LOWER(form_name) = %s AND status = 'pending'
    """
    g.db_cursor.execute(query, (form_name,))
    results = g.db_cursor.fetchall()

    if not results:
        return jsonify({"forms": []})

    # Convert result tuples to dictionaries
    form_list = [
        {
            "formId": row[0],
            "email": row[1],
            "formName": row[2],
            "status": row[3]
        }
        for row in results
    ]

    return jsonify({"forms": form_list})




if __name__ == "__main__":
    # Suppress Flask's default logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Suppress the default log messages

    # Your custom print statement
    print(f"Running on http://localhost:{app_config.PORT}")
    
    # Run the app
    app.run(host='0.0.0.0', port=app_config.PORT, use_reloader=False)
    