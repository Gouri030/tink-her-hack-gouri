// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDLOHk2kBmORGEytRX3tSkaOgKZ39wUOZg",
  authDomain: "travelbuddy-761bf.firebaseapp.com",
  projectId: "travelbuddy-761bf",
  storageBucket: "travelbuddy-761bf.firebasestorage.app",
  messagingSenderId: "269772207831",
  appId: "1:269772207831:web:f9c054d7fa3ba566726292",
  measurementId: "G-8M3GY06GFY"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);