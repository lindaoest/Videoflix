import os
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf import settings

# Function for user registration
def send_email_registration_task(instance, confirmation_msg_text, confirmation_msg_html):

	# Create email message
	msg = EmailMultiAlternatives(
            "Confirm your email",
            confirmation_msg_text,
            os.environ.get("EMAIL_HOST_USER"),
            [instance.email],
        )

	# Attach HTML version
	msg.attach_alternative(confirmation_msg_html, "text/html")

	# Attach logo
	relative_path = 'logo.png'
	# Get absolute path for logo
	image_path = os.path.join(settings.MEDIA_ROOT, relative_path)

	# Add logo to email header
	with open(image_path, 'rb') as img_file:
		image = MIMEImage(img_file.read())
		image.add_header('Content-ID', '<logo>')
		image.add_header('Content-Disposition', 'inline', filename='logo.png')
		msg.attach(image)

	# Send email
	msg.send()

# Function for password reset
def send_email_reset_password_task(instance, confirmation_msg_text, confirmation_msg_html):

	# Create email message
	msg = EmailMultiAlternatives(
            "Reset your password",
            confirmation_msg_text,
            os.environ.get("EMAIL_HOST_USER"),
            [instance.email],
        )

	# Attach HTML version
	msg.attach_alternative(confirmation_msg_html, "text/html")

	# Attach logo
	relative_path = 'logo.png'
	# Get absolute path for logo
	image_path = os.path.join(settings.MEDIA_ROOT, relative_path)

	# Add logo to email header
	with open(image_path, 'rb') as img_file:
		image = MIMEImage(img_file.read())
		image.add_header('Content-ID', '<logo>')
		image.add_header('Content-Disposition', 'inline', filename='logo.png')
		msg.attach(image)

	# Send email
	msg.send()