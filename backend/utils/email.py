from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
from ..config import settings
from .. import models

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_USER,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)

async def send_interview_invitation(interview: models.Interview, application: models.Application):
    template = Template("""
    Dear {{ candidate_name }},

    We are pleased to inform you that you have been shortlisted for the position of {{ job_title }}.

    Interview Details:
    Date and Time: {{ interview_time }}
    Type: {{ interview_type }}

    Please confirm your availability by clicking the following link:
    {{ confirmation_link }}

    Best regards,
    TalentMatch AI Team
    """)

    content = template.render(
        candidate_name=application.candidate.name,
        job_title=application.job.title,
        interview_time=interview.scheduled_time.strftime("%Y-%m-%d %H:%M"),
        interview_type=interview.interview_type,
        confirmation_link=f"http://localhost:8000/api/v1/interviews/confirm/{interview.id}"
    )

    message = MessageSchema(
        subject="Interview Invitation",
        recipients=[application.candidate.email],
        body=content,
        subtype="html"
    )

    fastmail = FastMail(conf)
    await fastmail.send_message(message)