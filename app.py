from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dataredundancysystem-d6b1d-default-rtdb.asia-southeast1.firebasedatabase.app'
})


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    ref = db.reference('users')
    existing_data = ref.get()

    # Check for duplicate email
    for key, value in (existing_data or {}).items():
        if value['email'] == email:
            return "Duplicate entry! Email already exists."

    # Add new data if email is unique
    ref.push({
        'name': name,
        'email': email
    })
    return "Successfully added unique data!"

if __name__ == '__main__':
    app.run(debug=True)
