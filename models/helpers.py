from datetime import datetime
import docx

from config import rake
import secrets
import string


def valid_datetime(date_input):
    date_format = "%m/%f/%Y"
    try:
        bool(datetime.strptime(date_input, date_format))
    except ValueError:
        return False

    return True


def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join((secrets.choice(characters) for _i in range(12)))


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def parse_resume_to_str(resume_obj):
    result = resume_obj.get('title', '') + "\n"
    sections = resume_obj.get('section', [])
    if len(sections) == 0:
        return result
    for sec in sections:
        if len(sec.get('experiences', [])) == 0:
            skills = sec.get('skills', [])
            for s in skills:
                skill = s.get('exp_data', {})
                title = skill.get('title', "") + " " if skill.get('title', "") != "" else ""
                result += title + "\n"
                description = skill.get('description', "")
                for d in description:
                    result += d + "\n"
        else:
            experiences = sec.get('experiences', [])
            for e in experiences:
                experience = e.get('exp_data', {})
                title = experience.get('title', "") + " " if experience.get('title', "") != "" else ""
                start_date = experience.get('start_date', "") + " " if experience.get('start_date', "") != "" else ""
                end_date = experience.get('end_date', "") + " " if experience.get('end_date', "") != "" else ""
                place = experience.get('place', "") + " " if experience.get('place', "") != "" else ""
                city_state = experience.get('city_state', "") + " " if experience.get('city_state', "") != "" else ""
                country = experience.get('country', "") + " " if experience.get('country', "") != "" else ""
                result += title + "\n" + start_date + end_date + "\n" + place + city_state + country
                description = experience.get('description', "")
                for d in description:
                    result += d + "\n"
    return result


def get_keywords(text):
    if len(text) == 0:
        return False, "No text to parse"
    keyword = {}
    rake.extract_keywords_from_text(text)
    keyword['ranked phrases'] = rake.get_ranked_phrases_with_scores()
    top_ten = keyword['ranked phrases'][:10]
    return True, top_ten
