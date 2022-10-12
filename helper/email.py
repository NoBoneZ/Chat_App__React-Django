from typing import Dict, Any

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template

from django.core.mail import EmailMessage


def new_send_mail_func(email_body: Dict[str, Any], context: Dict):
    """
    Send mail function to the specified email
    """
    print(email_body)
    try:
        message_template = get_template("accounts/password_mail.html").render(context)

        subject = email_body['subject']
        message = message_template
        email_from = settings.EMAIL_HOST_USER
        recipient_list = email_body['recipients']

        send_mail(
            subject,
            message,
            email_from,
            [recipient_list]
        )
        print(message)
        print(context["token"])

        print("email sent successfully")
    except Exception as e:
        print(e)
        return False
