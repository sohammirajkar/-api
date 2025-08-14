import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage

app = FastAPI(title="Soham Contact API")

# Allow cross-origin requests (so your frontend can call the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for contact form
class Contact(BaseModel):
    name: str
    email: str
    message: str

# Function to send email (optional)
def send_email(subject: str, body: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    to_email = os.getenv("TO_EMAIL")

    if not all([smtp_host, smtp_user, smtp_pass, to_email]):
        print("Email not configured; printing message instead:\n", body)
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)

# Contact endpoint
@app.post("/contact")
async def contact(c: Contact):
    body = f"From: {c.name} <{c.email}>\n\n{c.message}"
    send_email("New website contact", body)
    return {"status": "ok"}
