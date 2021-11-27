from flask import request, session, jsonify, render_template, url_for, flash
from email_validator import validate_email, EmailNotValidError
from werkzeug.utils import redirect

from config import app
from models.helpers import generate_random_password
from models.user import User


@app.route('/login', methods=['GET', 'POST'])  # define login page path
def login_user():
    if request.method == 'GET':  # if the request is a GET we return the login page
        return render_template('login.html')
    else:
        if request.json is not None:
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
                return jsonify({'success': False, 'message': 'Invalid email or password'})
        else:
            input_data = request.form
            email = input_data.get('email', '')
            password = input_data.get('password', '')
            try:
                email_results = validate_email(email)
                email = '{0}@{1}'.format(email_results.local_part.lower(), email_results.domain)
            except EmailNotValidError as ex:
                # Treat verification failure as normal login failure
                flash('Invalid email format')
                return redirect(url_for('register_user'))

            if User.login_valid(email, password):
                User.login(email)
                return redirect(url_for('profile'))
            else:
                session['email'] = None
                flash('Invalid email or password')
                return redirect(url_for('login_user'))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':  # If the request is GET we return the
        # sign up page and forms
        return render_template('signup.html')
    else:
        if request.json is not None:
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
                return jsonify({'success': False, 'mess age': message})
        else:
            input_data = request.form
            email = input_data.get('email', '')
            password = input_data.get('password', '')
            confirmed_password = input_data.get('confirmed_password', '')
            if password != confirmed_password:
                flash('Password does not match')
                return redirect(url_for('register_user'))
            try:
                email_results = validate_email(email)
                email = '{0}@{1}'.format(email_results.local_part.lower(), email_results.domain)
            except EmailNotValidError as ex:
                # Treat verification failure as normal login failure
                flash('Invalid email format')
                return redirect(url_for('register_user'))

            is_registered, message = User.register(email, password)
            if is_registered:
                flash('Sign up successfully')
                return redirect(url_for('login_user'))
            else:
                flash(message)
                return redirect(url_for('register_user'))


@app.route('/api/logout')
def api_logout_user():
    User.logout()
    if session['email'] is None:
        return jsonify({'success': True, 'message': 'Successfully logout'})
    else:
        return jsonify({'success': False, 'message': 'Error when logging out'})


@app.route('/logout')
def logout_user():
    User.logout()
    """
    if session['email'] is None:
        return jsonify({'success': True, 'message': 'Successfully logout'})
    else:
        return jsonify({'success': False, 'message': 'Error when logging out'})

    """
    return redirect(url_for('index'))
