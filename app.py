from flask import Flask, render_template, request
import os

app = Flask(__name__)
users  = {
    "name":"admin",
    "pass": "12345678"
}

age_cor = False


if not os.path.exists('uploads'):
    os.makedirs('uploads')
    

@app.route("/")
def home():
    return render_template("home.html")


@app.route('/upload', methods=['POST', 'GET'])
def upload():


    if request.method == "POST":

        loan_age = int(request.form.get("age"))
        if loan_age >= 18 and loan_age <= 65:
            print("fahad is gay")
        else:
            print("fhad is not gay")
            age_cor = True

        if age_cor == True:

            if 'aadhar_document' not in request.files:
                return "No file part", 400
            
            file = request.files['aadhar_document']
            
            if file.filename == '':
                return "No selected file", 400
            
            if file:
                filepath = os.path.join('uploads', file.filename)
                file.save(filepath)
                return f"File {file.filename} uploaded successfully!"
        

        
    return render_template("upload.html")
    

    
    


if __name__ == "__main__":
    app.run(debug=True)
