import logging

from django.contrib.auth import forms as auth_forms
from django.core.mail import EmailMultiAlternatives
from django.template import loader

logger = logging.getLogger(__name__)


class StrictPasswordResetForm(auth_forms.PasswordResetForm):
    """
    PasswordResetForm that lets email errors propagate.

    Django's default send_mail() swallows any exception and only logs the
    user pk to the 'django.contrib.auth' logger, so callers can't tell the
    email was not delivered. This version raises so the caller can log
    with proper context and react (e.g. warn the admin).
    """

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()


def send_password_setup_email(request, email):
    """
    Send Django's password reset email so the user can define a password.

    Returns True when the email was handed to the backend, False otherwise.
    Failures are logged instead of raised so the calling view can finish
    (the user record is already saved at that point).
    """
    form = StrictPasswordResetForm({'email': email})
    if not form.is_valid():
        logger.warning("Password email not sent: invalid address %r", email)
        return False

    try:
        form.save(use_https=request.is_secure(), request=request)
    except Exception:
        # SMTPException, socket errors, timeouts... none of them should 500 the request
        logger.exception(
            "Failed to send password email to %s (triggered by user %s)",
            email, request.user,
        )
        return False

    return True
