import datetime

from flask import request, jsonify
from config import app
from models.resume import Resume, Section, Experience, Skill


@app.route('/resume/get_all', methods=['GET'])
def get_all_resume():
    flag, message = Resume.get_resume_from_session()
    if flag:
        return jsonify({'success': True, 'data': message})
    return jsonify({'success': False, 'data': message})


@app.route('/resume/get/', methods=['GET'])
def get_resume():
    resume_id = request.args.get('resume_id')
    flag, message = Resume.get_resume_from_session(resume_id)
    if flag:
        return jsonify({'success': True, 'data': message})
    return jsonify({'success': False, 'message': message})


@app.route('/resume/add', methods=['POST'])
def add_resume():
    input_data = request.json
    title = input_data['title']
    flag, message = Resume.add_resume(title)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/resume/edit/<path:resume_id>', methods=['PUT'])
def edit_resume(resume_id):
    input_data = request.json
    title = input_data['title']
    flag, message = Resume.change_title(resume_id, title)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/resume/delete/', methods=['DELETE'])
def delete_resume():
    resume_id = request.args.get('resume_id')
    flag, message = Resume.delete_resume(resume_id)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/section/add/', methods=['POST'])
def add_section():
    input_data = request.json
    name = input_data['name']
    resume_id = request.args.get('resume_id')
    flag, message = Section.add_section(resume_id, name)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/section/get_all', methods=['GET'])
def get_all_section():
    resume_id = request.args.get('resume_id')
    flag, message = Section.get_section_from_session(resume_id)
    if flag:
        return jsonify({'success': True, 'data': message})
    return jsonify({'success': False, 'data': message})


@app.route('/section/get/', methods=['GET'])
def get_section():
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')
    flag, message = Section.get_section_from_session(resume_id, section_id)
    if flag:
        return jsonify({'success': True, 'data': message})
    return jsonify({'success': False, 'message': message})


@app.route('/section/edit/', methods=['PUT'])
def edit_section_name():
    input_data = request.json
    name = input_data['name']
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')
    flag, message = Section.edit_section_name(resume_id, section_id, name)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/section/delete/', methods=['DELETE'])
def delete_section():
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')
    flag, message = Section.delete_section(resume_id, section_id)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/experience/add/', methods=['POST'])
def add_experience():
    input_data = request.json
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')

    flag, message = Experience.add_experience(resume_id, section_id, input_data['data'])
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/experience/edit/', methods=['PUT'])
def edit_experience():
    input_data = request.json
    if not input_data:
        return jsonify({'success': False, 'message': "Nothing change"})
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')
    experience_id = request.args.get('experience_id')
    flag, message = Experience.edit_experience(resume_id, section_id, experience_id, input_data)

    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/experience/delete/', methods=['DELETE'])
def delete_experience():
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')
    experience_id = request.args.get('experience_id')
    flag, message = Experience.delete_experience(resume_id, section_id, experience_id)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/skill/add/', methods=['POST'])
def add_skill():
    input_data = request.json
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')

    flag, message = Skill.add_skill(resume_id, section_id, input_data['data'])
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/skill/edit/', methods=['PUT'])
def edit_skill():
    input_data = request.json
    if not input_data:
        return jsonify({'success': False, 'message': "Nothing change"})
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')
    skill_id = request.args.get('skill_id')
    flag, message = Experience.edit_experience(resume_id, section_id, skill_id, input_data)

    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/skill/delete/', methods=['DELETE'])
def delete_skill():
    resume_id = request.args.get('resume_id')
    section_id = request.args.get('section_id')
    skill_id = request.args.get('skill_id')
    flag, message = Experience.delete_experience(resume_id, section_id, skill_id)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})
