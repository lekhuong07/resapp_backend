from datetime import datetime
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
