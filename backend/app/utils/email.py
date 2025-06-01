from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..config import settings
from .. import models
from jinja2 import Template
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_USER,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

class EmailClient:
    def __init__(self):
        self.conf = conf
        self.fastmail = FastMail(self.conf)

    async def send_interview_invitation(
        self,
        interview: models.Interview,
        application: models.Application
    ) -> None:
        template = Template("""
        Dear {{ candidate_name }},

        You have been shortlisted for the position of {{ job_title }}.
        Your interview has been scheduled for {{ interview_time }}.

        Interview Details:
        Type: {{ interview_type }}
        Notes: {{ notes }}

        Please confirm your availability by clicking the link below:
        {{ confirmation_link }}

        Best regards,
        TalentMatch AI Team
        """)

        content = template.render(
            candidate_name=application.candidate.name,
            job_title=application.job.title,
            interview_time=interview.scheduled_time.strftime("%Y-%m-%d %H:%M"),
            interview_type=interview.interview_type,
            notes=interview.notes or "",
            confirmation_link=f"http://localhost:8000/api/v1/interviews/confirm/{interview.id}"
        )

        message = MessageSchema(
            subject="Interview Invitation",
            recipients=[application.candidate.email],
            body=content,
            subtype="html"
        )

        await self.fastmail.send_message(message)

    async def send_password_reset_email(self, user: models.User, reset_token: str) -> None:
        template = Template("""
        Dear {{ user_name }},

        You requested to reset your password. Please click the link below to reset your password:
        {{ reset_link }}

        If you did not request this, please ignore this email.

        Best regards,
        TalentMatch AI Team
        """)

        content = template.render(
            user_name=user.name,
            reset_link=f"http://localhost:8000/reset-password?token={reset_token}"
        )

        message = MessageSchema(
            subject="Password Reset Request",
            recipients=[user.email],
            body=content,
            subtype="html"
        )

        await self.fastmail.send_message(message)

    async def send_welcome_email(self, user: models.User) -> None:
        template = Template("""
        Dear {{ user_name }},

        Welcome to TalentMatch AI! We are excited to have you on board.

        You can start exploring job opportunities and manage your applications easily.

        Best regards,
        TalentMatch AI Team
        """)

        content = template.render(
            user_name=user.name
        )

        message = MessageSchema(
            subject="Welcome to TalentMatch AI",
            recipients=[user.email],
            body=content,
            subtype="html"
        )

        await self.fastmail.send_message(message)

    async def send_application_confirmation_email(self, application: models.Application) -> None:
        template = Template("""
        Dear {{ candidate_name }},

        Your application for the position of {{ job_title }} has been successfully submitted.

        We will review your application and get back to you shortly.

        Best regards,
        TalentMatch AI Team
        """)

        content = template.render(
            candidate_name=application.candidate.name,
            job_title=application.job.title
        )

        message = MessageSchema(
            subject="Application Confirmation",
            recipients=[application.candidate.email],
            body=content,
            subtype="html"
        )

        await self.fastmail.send_message(message)

# Create a singleton instance
email_client = EmailClient()

# Export the send functions for use in other modules
async def send_interview_invitation(interview: models.Interview, application: models.Application):
    await email_client.send_interview_invitation(interview, application)

async def send_password_reset_email(user: models.User, reset_token: str):
    await email_client.send_password_reset_email(user, reset_token)

async def send_welcome_email(user: models.User):
    await email_client.send_welcome_email(user)

async def send_application_confirmation_email(application: models.Application):
    await email_client.send_application_confirmation_email(application)