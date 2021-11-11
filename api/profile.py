import datetime
import json

from flask import request, session, jsonify
from email_validator import validate_email, EmailNotValidError
from config import app
from models.user import User


@app.route('/profile/get', methods=['GET'])
def get_profile():
    flag, message = User.get_profile()
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/profile/edit', methods=['PUT'])
def edit_profile():
    input_data = request.json
    name = input_data.get('name', '')
    dob = input_data.get('dob', '')
    statement = input_data.get('statement', '')
    flag, message = User.edit_profile(name, dob, statement)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/password/edit', methods=['PUT'])
def edit_password():
    input_data = request.json
    email = input_data.get('email', '')
    new_password = input_data.get('new_password', '')
    confirmed_new_password = input_data.get('confirmed_new_password', '')
    if new_password != confirmed_new_password:
        return jsonify({'success': False, 'message': 'Confirmed password does not match'})

    try:
        email_results = validate_email(email)
        email = '{0}@{1}'.format(email_results.local_part.lower(), email_results.domain)
    except EmailNotValidError as ex:
        # Treat verification failure as normal login failure
        return jsonify({'success': False, 'message': 'Invalid email format'})

    flag, message = User.change_password(email, new_password)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/password/forgot', methods=['POST'])
def reset_password():
    input_data = request.json
    email = input_data.get('email', '')
    return User.reset_password(email)


@app.route('/application/add', methods=['POST'])
def add_application():
    input_data = request.json
    company = input_data['company']
    position = input_data['position']
    flag, message = User.add_application(company, position)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/application/get_all', methods=['GET'])
def get_all_application():
    flag, message = User.get_application()
    if flag:
        return jsonify({'success': True, 'data': message})
    return jsonify({'success': False, 'data': message})


@app.route('/application/get/<path:application_id>', methods=['GET'])
def get_application(application_id):
    flag, message = User.get_application(application_id)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/application/next_step/<path:application_id>', methods=['PUT'])
def update_application(application_id):
    input_data = request.json
    status = input_data['status']
    flag, message = User.update_application(application_id, status)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/application/delete/<path:application_id>', methods=['DELETE'])
def delete_application(application_id):
    flag, message = User.delete_application(application_id)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})
