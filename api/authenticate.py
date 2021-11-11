from flask import request, session, jsonify
from email_validator import validate_email, EmailNotValidError
from config import app
from models.helpers import generate_random_password
from models.user import User


@app.route('/login', methods=['POST'])
def login_user():
    input_data = request.json
    email = input_data.get('email', '')
    password = input_data.get('password', '')
    try:
        email_results = validate_email(email)
        email = '{0}@{1}'.format(email_results.local_part.lower(), email_results.domain)
    except EmailNotValidError as ex:
        # Treat verification failure as normal login failure
        return jsonify({'success': False, 'message': 'Invalid email'})

    if User.login_valid(email, password):
        User.login(email)
        return jsonify({'success': True, 'email': email})
    else:
        session['email'] = None
        return jsonify({'success': False, 'message': 'Invalid email or password'})


@app.route('/register', methods=['POST'])
def register_user():
    input_data = request.json
    email = input_data.get('email', '')
    password = input_data.get('password', '')
    confirmed_password = input_data.get('confirmed_password', '')
    if password != confirmed_password:
        return jsonify({'success': False, 'message': 'Password does not match'})

    try:
        email_results = validate_email(email)
        email = '{0}@{1}'.format(email_results.local_part.lower(), email_results.domain)
    except EmailNotValidError as ex:
        # Treat verification failure as normal login failure
        return jsonify({'success': False, 'message': 'Invalid email format'})

    is_registered, message = User.register(email, password)
    if is_registered:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message})


@app.route('/logout', methods=['POST'])
def logout_user():
    User.logout()
    if session['email'] is None:
        return jsonify({'success': True, 'message': 'Successfully logout'})
    else:
        return jsonify({'success': False, 'message': 'Error when logging out'})
