import random

from django.core.mail import send_mail, BadHeaderError


def generate_key(length=None):

    if length is None:
        length = 32
    digits='1234567890'
    letters='qwertyuiopasdfghjklzcvbnm'
    uletters = letters.upper()
    blank = digits + letters + uletters
    lst = list(blank)
    random.shuffle(lst)
    key = ''.join([random.choice(lst) for _ in range(length)])
    return key

def send_email(email, code):
    """Отправка кода на email"""
    subject = 'Код подтверждения LAUTAVITO'
    message = 'Введите этот код для подтверждения email на сайте LAUTAVITO: {}'.format(code)
    try:
        send_mail(subject, message, 'emailsenddjango@gmail.com', [email])
        return True
    except BadHeaderError:
        return False
