import random
from django.core.mail import send_mail

def generate_code():
    return str(random.randint(100000, 999999))

def send_verification_code(email, code):
    code = generate_code()
    send_mail(
        'Tasdiqlash kodi',
        f'Sizning tasdiqlash kodingiz: {code}',
        'noreply@yourdomain.com',
        [email],
        fail_silently=False,
    )
