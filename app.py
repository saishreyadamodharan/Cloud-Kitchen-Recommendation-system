from flask import Flask, render_template, request, redirect, url_for, flash
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulate a database with dictionaries
users_db = {}
payments_db = {}

# Path to CSV file
PRODUCTS_CSV = 'products.csv'

# Home Route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication check
        if username in users_db and users_db[username]['password'] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('recommend'))
        else:
            flash('Invalid credentials, please try again.', 'error')
    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        # Simple validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))
        
        if username not in users_db:
            users_db[username] = {'email': email, 'password': password}
            flash('Account created successfully!', 'success')
            return redirect(url_for('recommend'))
        else:
            flash('Username already exists.', 'error')
    return render_template('signup.html')

# Payment Route
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        card_number = request.form['card_number']
        expiration = request.form['expiration']
        cvv = request.form['cvv']

        # Simple payment validation
        if len(card_number) != 16 or len(cvv) != 3:
            flash('Invalid payment details.', 'error')
            return redirect(url_for('payment'))
        
        payments_db[card_number] = {'expiration': expiration, 'cvv': cvv}
        flash('Payment successful! Thank you for your purchase.', 'success')
        return redirect(url_for('home'))
    return render_template('payment.html')

# Recommendation Route (New page after login/signup)
@app.route('/recommend')
def recommend():
    # Read the products from the CSV file
    products = read_products_from_csv('Cloud Dataset.csv')
    
    # Here, we can filter or sort products based on the user's preferences
    # For simplicity, we'll just return all products for now
    return render_template('recommend.html', products=products)

# Function to read products from CSV file
def read_products_from_csv(file_path):
    products = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                products.append(row)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return products

if __name__ == '__main__':
    app.run(debug=True)
