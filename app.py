from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# User credentials
users = {
    "name": "Zaid",
    "pass": "12345678"
}

# In-memory storage for user data
user_data = {}
credit_score = 0

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == users["name"] and password == users["pass"]:
            session['logged_in'] = True
            return redirect("/home")
        else:
            return "User  not found", 404   
    return render_template("login.html")

@app.route("/")
def index():
    return redirect("/login")

@app.route("/home")
def home():
    if session.get('logged_in'):
        return render_template("home.html", users=users, credit_score=credit_score)
    else:
        return 'You have to log in first'

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    global credit_score
    if request.method == "POST":
        loan_name = request.form.get("name")
        loan_age = int(request.form.get("age"))
        no_fam = request.form.get("no_fam")
        
        # Validate age
        if loan_age < 18 or loan_age > 65:
            return "Age is not suitable for a loan", 400
        
        family_income = int(request.form.get("inc_fam"))

        # Calculate credit score based on family income
        if family_income < 1000:
            credit_score += 0
        elif family_income <= 10000:
            credit_score += 10
        elif family_income <= 30000:
            credit_score += 20
        elif family_income <= 50000:
            credit_score += 30
        elif family_income <= 70000:
            credit_score += 40
        elif family_income <= 90000:
            credit_score += 50
        else:
            credit_score += 60

        # Check for file upload
        if 'aadhar_document' not in request.files:
            return "No file part", 400
        
        file = request.files['aadhar_document']
        if file.filename == '':
            return "No selected file", 400
        
        if file:
            filepath = os.path.join('uploads', file.filename)
            file.save(filepath)

            # Store user data
            user_data[loan_name] = {
                "loan_age": loan_age,
                "no_fam": no_fam,
                "family_income": family_income,
                "credit_score": credit_score
            }

            return redirect("/home")  # Redirect to home after successful upload

    if session.get('logged_in'):
        return render_template("upload.html")
    else:
        return "You have to log in first"

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/data")
def data():
    return render_template("data.html", user_data=user_data)

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)