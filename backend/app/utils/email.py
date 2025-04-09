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

# Create a singleton instance
email_client = EmailClient()

# Export the send function for use in other modules
async def send_interview_invitation(interview: models.Interview, application: models.Application):
    await email_client.send_interview_invitation(interview, application)