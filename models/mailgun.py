import os
from requests import Response, post


class MailgunExceptionError(Exception):
    def __init__(self, message):
        self.message = message


class Mailgun:
    FROM_TITLE = 'Reset password'
    FROM_EMAIL = 'do-not-reply@sandboxa1837cf9d8d64ad893dbadf4d2102a4f.mailgun.org'

    @classmethod
    def send_mail(cls, email, subject, text, html=None):
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)

        if api_key is None:
            return False, MailgunExceptionError('Failed to load Mailgun API key.')

        if domain is None:
            return False, MailgunExceptionError('Failed to load Mailgun Domain.')

        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                              "to": email,
                              "subject": subject,
                              "text": text,
                              "html": html}
                        )
        if response.status_code != 200:
            return False, MailgunExceptionError('There is an error happen while sending e-mail.')
        return True, 'Email sent successfully'
