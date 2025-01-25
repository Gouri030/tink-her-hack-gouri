from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin.exceptions import FirebaseError
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte string

# Initialize Firebase
cred = credentials.Certificate("database/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Access Firestore database
db = firestore.client()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login page if not logged in

# User session model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader callback to load user from session
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for("register"))

        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
            )

            # Store user details in Firestore
            user_ref = db.collection("users").document(email)
            user_ref.set({
                "name": name,
                "age": age,
                "email": email,
                "destination": "",
                "interest": "",
                "travel_dates": {
                    "start_date": "",
                    "end_date": ""
                }
            })

            flash("User registered successfully!")
            return redirect(url_for("login"))

        except FirebaseError as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for("register"))

    return render_template("register.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Authenticate user with Firebase Authentication using email and password
            user = auth.get_user_by_email(email)  # Check if the user exists
            
            # Validate password (Firebase handles the verification automatically)
            user_data = auth.get_user(user.uid)

            if user_data:
                login_user(User(user_data.uid))  # login the user using Flask-Login
                flash("Login successful!")
                return redirect(url_for("home"))  # Redirect to home or another page where the user can find buddies

            else:
                flash("Invalid email or password. Please try again.")
                return render_template("login.html", error="Invalid email or password")

        except firebase_admin.auth.UserNotFoundError:
            flash("User not found. Please check your email and try again.")
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Home page route (for showing registered user)
@app.route("/", methods=["GET", "POST"])
@login_required  # Protect this route to ensure the user is logged in
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        interest = request.form["interest"]
        destination = request.form["destination"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Firestore document structure
        user_data = {
            "name": name,
            "email": email,
            "destination": destination,
            "interest": interest,
            "travel_dates": {
                "start_date": start_date,
                "end_date": end_date
            }
        }

        # Save data to Firestore under the 'users' collection
        db.collection("users").add(user_data)

        return render_template("buddy.html", name=name, destination=destination, start_date=start_date, end_date=end_date)

    return render_template("index.html")

# Find Buddies Route (for showing users with matching destinations and interests)
@app.route("/find_buddies", methods=["GET"])
@login_required  # Protect this route to ensure the user is logged in
def find_buddies():
    user_email = current_user.id  # Get the email of the logged-in user from Flask-Login
    user_ref = db.collection("users").document(user_email)
    user = user_ref.get().to_dict()

    # Get user details
    destination = user["destination"]
    interest = user["interest"]
    start_date = datetime.strptime(user["travel_dates"]["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(user["travel_dates"]["end_date"], "%Y-%m-%d")

    # Query Firestore for users with matching destination and interest
    matching_users = db.collection("users").where("destination", "==", destination).where("interest", "==", interest).stream()

    buddies = []
    for buddy in matching_users:
        buddy_data = buddy.to_dict()

        # Get buddy's travel dates
        buddy_start_date = datetime.strptime(buddy_data["travel_dates"]["start_date"], "%Y-%m-%d")
        buddy_end_date = datetime.strptime(buddy_data["travel_dates"]["end_date"], "%Y-%m-%d")

        # Check if travel dates overlap (simple comparison logic, you can improve this)
        if start_date <= buddy_end_date and end_date >= buddy_start_date:
            buddies.append({
                "name": buddy_data["name"],
                "email": buddy_data["email"],
                "destination": buddy_data["destination"],
                "interest": buddy_data["interest"],
                "start_date": buddy_data["travel_dates"]["start_date"],
                "end_date": buddy_data["travel_dates"]["end_date"]
            })

    return render_template("buddies.html", buddies=buddies)

if __name__ == "__main__":
    app.run(debug=True)
