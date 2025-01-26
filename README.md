# Project Name - WanderGuard🎯


## Basic Details

### Team Members
- Member 1: Gouri K - Amrita Vishwavidyapeetham, Amritapuri


### Hosted Project Link
[mention your project hosted project link here]

### Project Description
Travel Buddy is a platform that helps users find travel companions based on shared interests and destinations. By providing travel details like dates, destination, and preferences, users can easily connect with others who are traveling to the same place during the same time.

### The Problem statement
Traveling solo can be lonely, expensive, and sometimes a little intimidating. Finding someone who shares your interests and travel plans shouldn’t be a challenge. That's where Travel Buddy steps in – matching like-minded travelers looking for company.

### The Solution
With Travel Buddy, finding a travel buddy is as easy as sharing your destination and interest! By inputting travel dates, destination, and interests, the platform will show you potential travel companions who are going to the same places and share the same passion for travel. No more lonely trips!

## Technical Details
### Technologies/Components Used
For Software:

Languages used: Python, HTML, CSS, JavaScript
Frameworks used: Flask (Backend), Bootstrap (Frontend)
Libraries used: Firebase SDK, Jinja2 (for templating), DateTime (for date operations)
Tools used: Firebase (for database and authentication), Vercel for hosting and database management.

### Implementation
For Software:
# Installation
Installation
To set up the project on your local machine, follow these steps:

Clone the repository
Clone the Travel Buddy repository to your local machine using the following command:
git clone <repository-url>

Navigate to the project directory
Change your directory to the project folder:
cd <repository-address>

Download all the dependancies 
 pip install <Dependancies listed in requirements.txt>

# Run
python app.py

### Project Documentation
For Software:

Frontend

The frontend of this project uses HTML, CSS (with Bootstrap), and JavaScript. The layout is designed for a clean and responsive user experience.
The index.html serves as the homepage where users input their travel details, while buddies.html displays the list of potential travel buddies.

Backend

Flask handles the server-side logic, routing, and user authentication. Firebase is used to store user data, including travel details, and manage user authentication via Firebase Auth.
The application logic checks for matching travel buddies by comparing users' destination, interests, and travel dates in the Firebase database.

User Authentication

Firebase Authentication is used to securely manage user sign-ups, logins, and sessions.
Database

Firebase Firestore is used to store user data. Each user document contains details like name, email, destination, interest, and travel_dates.

FUTURE SCOPE:

### **1. AI-Powered Trip Planner (Core Feature)**

This feature is the backbone of your platform, combining safety and planning for solo travelers.

- **Why focus on it?** It showcases the platform's core purpose: empowering users with safe, well-planned trips tailored to their preferences.
- **What to implement?**
    - A simple form where users can input preferences (destination, travel style).
    - Use the **Google Maps API** to:
        - Suggest safe routes.
        - Highlight safety zones on maps.
    - Display the itinerary (e.g., stops, attractions) dynamically in the UI.
- **Execution Time:**
    - **Backend:** 2–3 hours (Flask route + API integration).
    - **Frontend:** 2–3 hours (HTML, CSS, JavaScript to display results).

### **2.Regional Slang Translation & Cultural Guidance**

- **AI-Powered Translation Tool**
    - Powered by NLP (Natural Language Processing), Wander Guard translates regional slang, such as Malayalam phrases, into English in real time.
    - This feature enhances communication in unfamiliar places, breaking down language barriers.
- Powered by NLP (Natural Language Processing), Wander Guard translates regional slang, such as Malayalam phrases, into English in real time.
- This feature enhances communication in unfamiliar places, breaking down language barriers.



# Screenshots (Add at least 3)
!![Login Page](assets/images/Screenshot%202025-01-26%20094657.png)

![Registeration](assets/images/Screenshot%202025-01-26%20101119.png)

![Travel Buddy Interface](assets/images/Screenshot%202025-01-26%20094802.png)

!![Displays Matching Buddies](assets/images/Screenshot%202025-01-26%20094815.png)

# Diagrams
![flow chart](assets/images/Screenshot%202025-01-26%20102110.png)

### Project Demo
# Video
[DEMO VIDEO]
*Explain what the video demonstrates*](https://drive.google.com/file/d/1T7lN3xSB3Y56y8bM8ST2iAsC15k_qV0_/view?usp=sharing)

Video Description:
This video showcases the process of how the Travel Buddy platform works. It demonstrates the following key steps:

User Registration & Login: A user creates an account by entering their name, age, and email, or logs in if they already have an account.
Entering Travel Details: Once logged in, the user proceeds to the main page where they input their travel details, including their destination, interests, and travel dates.
Finding a Travel Buddy: The user clicks on the "Find Buddy" button, which triggers a search for other users with matching travel destinations, interests, and dates.
Buddy Listing: After the search, the matching travel buddies are displayed in a list, allowing users to connect with potential companions for their travels.

Made with ❤️ at TinkerHub
