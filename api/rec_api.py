from models.helpers import parse_resume_to_str, get_keywords
from models.user import User
from models.resume import Resume

from flask import request, jsonify
from config import app

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


"""
!pip install nlp
!pip install PyPDF2==1.26.0
!pip install textract
!pip install fuzzywuzzy
from gensim.summarization.summarizer import summarize
"""


@app.route('/recommendation/get_resume_text/', methods=['GET'])
def get_resume_text():
    flag_profile, message_profile = User.get_profile()
    if flag_profile:
        resume_id = request.args.get('resume_id')
        flag, message = Resume.get_resumes_from_session(resume_id)
        if flag:
            result = parse_resume_to_str(message, message_profile["ps"])
            return jsonify({'success': True, 'message': result})
        return jsonify({'success': False, 'message': message})
    return jsonify({'success': False, 'message': message_profile})


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
    flag_profile, message_profile = User.get_profile()
    if flag_profile:
        flag, message = Resume.get_resumes_from_session()
        if flag:
            if len(message) > 0:
                jd = input_data['job_description']
                flag_words, words = get_keywords(jd)
                if not flag_words:
                    return jsonify({'success': False, 'message': words})
                keywords = []
                for w in words:
                    keywords.append(w[1] + ": " + str(round(w[0], 2)))
                similarity = [jd]
                titles = []
                for res in message:
                    resume_text = parse_resume_to_str(res, message_profile["ps"])
                    titles.append(res["title"])
                    similarity.append(resume_text)
                cv = CountVectorizer()
                count_matrix = cv.fit_transform(similarity)
                result = [str(round(r, 2)) + " %" for r in cosine_similarity(count_matrix)[0]*100][1:]
                results = []
                for i, r in enumerate(result):
                    results.append(titles[i] + ": " + r)
                return jsonify({'success': True, 'message': {"keywords": keywords, "similarity": results}})
            return jsonify({'success': False, 'message': "No experiences to parse"})
        return jsonify({'success': False, 'message': message})
    return jsonify({'success': False, 'message': message_profile})
