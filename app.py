from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin.exceptions import FirebaseError
from datetime import datetime, timedelta
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
                login_user(User(user_data.uid))  # Login the user using Flask-Login
                flash("Login successful!")
                return redirect(url_for("home"))  # Redirect to home page

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

# Home page route
@app.route("/", methods=["GET", "POST"])
@login_required
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

# Find Buddies Route
from datetime import datetime
from flask import render_template, current_app
from flask_login import login_required, current_user

@app.route("/find_buddies", methods=["GET"])
@login_required
def find_buddies():
    # Retrieve the current user's email and reference from Firestore
    user_email = current_user.id
    user_ref = db.collection("users").document(user_email)
    
    try:
        # Get the user data from Firestore
        user = user_ref.get().to_dict()
        if not user:
            return "User data not found", 404
        
        # Extract destination, interest, and travel dates
        destination = user.get("destination")
        interest = user.get("interest")
        travel_dates = user.get("travel_dates", {})
        start_date_str = travel_dates.get("start_date")
        end_date_str = travel_dates.get("end_date")
        
        # If any required field is missing, handle the error
        if not destination or not interest or not start_date_str or not end_date_str:
            return "Incomplete user data", 400

        # Convert start and end dates to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        # Query for users with the same destination and interest
        matching_users = db.collection("users").where("destination", "==", destination)\
                                                .where("interest", "==", interest).stream()
        
        buddies = []
        
        # Loop through the matching users and filter based on travel dates overlap
        for buddy in matching_users:
            buddy_data = buddy.to_dict()
            buddy_start_date = datetime.strptime(buddy_data["travel_dates"]["start_date"], "%Y-%m-%d")
            buddy_end_date = datetime.strptime(buddy_data["travel_dates"]["end_date"], "%Y-%m-%d")

            # Check if the travel dates overlap
            if start_date <= buddy_end_date and end_date >= buddy_start_date:
                buddies.append({
                    "name": buddy_data["name"],
                    "email": buddy_data["email"],
                    "destination": buddy_data["destination"],
                    "interest": buddy_data["interest"],
                    "start_date": buddy_data["travel_dates"]["start_date"],
                    "end_date": buddy_data["travel_dates"]["end_date"]
                })

        # If no matching buddies, you can show a message or an empty list
        if not buddies:
            current_app.logger.info(f"No buddies found for user: {user_email}")
            return render_template("buddies.html", buddies=None)  # Or display a message in the template

        # Return the list of matching buddies
        return render_template("buddies.html", buddies=buddies)

    except Exception as e:
        # Catch and log any errors
        current_app.logger.error(f"Error finding buddies: {e}")
        return "An error occurred while finding buddies", 500


if __name__ == "__main__":
    app.run(debug=True)
