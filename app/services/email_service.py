from email.mime.text import MIMEText
import smtplib
import os


class EmailSendingFailed(Exception):
    pass


class EmailService:
    def send_verification_email(self, user, verification_code):
        msg = MIMEText(f"Your verification code is {verification_code}")
        msg["Subject"] = "Verify your email address"
        msg["From"] = "register@no-reply.com"
        msg["To"] = user.email
        try:
            with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")) as s:
                s.send_message(msg)
        except Exception as e:
            raise EmailSendingFailed(f"Failed to send email: {e}")
