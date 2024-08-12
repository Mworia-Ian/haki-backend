## Installation of packages
### pipenv install flask Flask-SQLAlchemy Flask-Cors sqlalchemy-serializer flask-bcrypt Flask-Migrate flask-restful flask-jwt-extended python-dotenv


Use npm

If you're already using npm and a module bundler such as webpack or Rollup, you can run the following command to install the latest SDK (Learn more):

npm install firebase
Then, initialize Firebase and begin using the SDKs for the products you'd like to use.

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAXb27yUzejHkMSnzNgNROO5Tze_Kdrb-g",
  authDomain: "haki-1aa36.firebaseapp.com",
  projectId: "haki-1aa36",
  storageBucket: "haki-1aa36.appspot.com",
  messagingSenderId: "725550450284",
  appId: "1:725550450284:web:bf154d7b3266f1de2a3a49",
  measurementId: "G-2P8621TR5P"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
Note: This option uses the modular JavaScript SDK, which provides reduced SDK size.

Learn more about Firebase for web: Get Started, Web SDK API Reference, Samples

To host your site with Firebase Hosting, you need the Firebase CLI (a command line tool).

Run the following npm command to install the CLI or update to the latest CLI version.

npm install -g firebase-tools
Doesn't work? Take a look at the Firebase CLI reference or change your npm permissions
