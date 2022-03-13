from models.helpers import parse_resume_to_str, get_keywords
from models.resume import Resume

from flask import request, jsonify
from config import app

"""
!pip install nlp
!pip install PyPDF2==1.26.0
!pip install textract
!pip install fuzzywuzzy
from gensim.summarization.summarizer import summarize
"""


@app.route('/recommendation/get_text/', methods=['GET'])
def get_resume_text():
    resume_id = request.args.get('resume_id')
    flag, message = Resume.get_resume_from_session(resume_id)
    if flag:
        result = parse_resume_to_str(message['data'])

    return jsonify({'success': False, 'message': message})


@app.route('/recommendation/keyword_text/', methods=['GET'])
def get_keyword_text():
    input_data = request.json
    text_data = input_data['text']
    flag, message = get_keywords(text_data)
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})


@app.route('/recommendation/similarity/', methods=['GET'])
def get_similarity():
    input_data = request.json
    text_data = input_data['text']
    flag, message = Resume.get_resume_from_session()
    if flag:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message})
