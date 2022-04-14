import random

from django.core.mail import send_mail, BadHeaderError


def generate_code_email(len=20):
    letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
    lower_letters = letters.lower()
    digits = "1234567890"
    blank = list(letters+lower_letters+digits)
    random.shuffle(blank)
    return "".join([random.choice(blank) for x in range(len)])

def send_email(email, code):

    subject = 'Код подтверждения Django Shop'
    message = 'Введите этот код подтверждения email: {}'.format(code)
    try:
        send_mail(subject, message, 'emailsenddjango@gmail.com', [email])
        return True
    except BadHeaderError:
        return False