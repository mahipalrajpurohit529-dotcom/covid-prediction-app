# ============================================================
# app.py - Main Flask Application
# Flask + MySQL + Machine Learning Web App
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import joblib
import pandas as pd

app = Flask(__name__)
app.secret_key = "6378"



# ============================================================
# DATABASE CONNECTION
# ============================================================
def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="----",   # <-- Change this
        database="ml_app",
        cursorclass=pymysql.cursors.DictCursor  # Returns rows as dictionaries
    )
    return connection





# ============================================================
# LOAD THE TRAINED ML MODEL
# ============================================================
model = joblib.load("lr_model.pkl")



# ============================================================
# HOME - Redirect to login page
# ============================================================
@app.route("/")
def home():
    return redirect(url_for("login"))



# ============================================================
# REGISTER - Create a new account
# ============================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new user into the users table
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")




# ============================================================
# LOGIN - Verify credentials and start a session
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username and password match a record in users table
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # Save user_id in the session so we know who is logged in
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again."

    return render_template("login.html", error=error)


# ============================================================
# LOGOUT - Clear the session
# ============================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



# ============================================================
# DASHBOARD - Main page after login
# Only accessible to logged-in users
# ============================================================
@app.route("/dashboard")
def dashboard():
    # If user is not logged in, send them to login page
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])




# ============================================================
# PREDICT - Run the ML model and save result
# ============================================================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user_id" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":
        # Collect form inputs
        age    = int(request.form["age"])
        gender = request.form["gender"]
        fever  = int(request.form["fever"])
        cough  = request.form["cough"]
        city   = request.form["city"]


        input_df = pd.DataFrame(
        [[age, gender, fever, cough, city]],
        columns=['age', 'gender', 'fever', 'cough', 'city']
        )
        prediction = model.predict(input_df)[0]
        result = str(prediction)

        # Save the prediction to the database, linked to current user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO predictions (user_id, age, gender, fever, cough, city, result) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (session["user_id"], age, gender, fever, cough, city, result)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return render_template("predict.html", result=result)





# ============================================================
# HISTORY - Show this user's past predictions
# ============================================================
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch only the predictions that belong to the logged-in user
    cursor.execute(
        "SELECT * FROM predictions WHERE user_id = %s",
        (session["user_id"],)
    )
    predictions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("history.html", predictions=predictions)





# ============================================================
# BOOK SERVICE - Submit a service booking
# ============================================================
@app.route("/service", methods=["GET", "POST"])
def service():
    if "user_id" not in session:
        return redirect(url_for("login"))

    success = False

    if request.method == "POST":
        service_name = request.form["service"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Save the service booking linked to the current user
        cursor.execute(
            "INSERT INTO services (user_id, service) VALUES (%s, %s)",
            (session["user_id"], service_name)
        )
        conn.commit()
        cursor.close()
        conn.close()

        success = True

    return render_template("service.html", success=success)





# ============================================================
# CONTACT - Submit a message
# ============================================================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if "user_id" not in session:
        return redirect(url_for("login"))

    success = False

    if request.method == "POST":
        message = request.form["message"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Save the message linked to the current user
        cursor.execute(
            "INSERT INTO messages (user_id, message) VALUES (%s, %s)",
            (session["user_id"], message)
        )
        conn.commit()
        cursor.close()
        conn.close()

        success = True

    return render_template("contact.html", success=success)





# ============================================================
# RUN THE APP
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
