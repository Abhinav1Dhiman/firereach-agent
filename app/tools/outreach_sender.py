import smtplib
from email.mime.text import MIMEText
from groq import Groq
from app.config import GROQ_API_KEY, EMAIL_USER, EMAIL_PASS

client = Groq(api_key=GROQ_API_KEY)

def tool_outreach_automated_sender(brief, email):

    prompt = f"""
Write a short hyper-personalized cold email based on:

{brief}

Rules:
- Mention the signals
- No templates
- Human tone
- Under 120 words
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}]
    )

    email_text = response.choices[0].message.content

    msg = MIMEText(email_text)
    msg["Subject"] = "Quick idea"
    msg["From"] = EMAIL_USER
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        return {
            "status": "sent",
            "email": email_text
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "email": email_text
        }