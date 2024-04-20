// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCRFc8oHJOTtO-uDImaq7QzPMMOkR-T9Bk",
  authDomain: "nepali-ocr-eb600.firebaseapp.com",
  projectId: "nepali-ocr-eb600",
  storageBucket: "nepali-ocr-eb600.appspot.com",
  messagingSenderId: "726096230656",
  appId: "1:726096230656:web:2007b359138812db6f5be5",
  measurementId: "G-D90JT77CRJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);