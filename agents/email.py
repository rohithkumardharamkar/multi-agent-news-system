import smtplib
from email.mime.text import MIMEText
from config.settings import EMAIL_USER, EMAIL_PASSWORD, EMAIL_TO, EMAIL_HOST, EMAIL_PORT

def email_agent(state):
    logs = state.get("logs", [])
    report = state.get("magazine_report", "")
    if not report:
        return {"email_status": "No report to send", "logs": logs}
    target_email = state.get("target_email") or EMAIL_TO
    if not EMAIL_USER or not EMAIL_PASSWORD or not target_email:
        return {"email_status": "Email not configured - report generated successfully", "logs": logs}
    try:
        msg = MIMEText(report)
        msg["Subject"] = "Daily AI News Magazine Digest"
        msg["From"] = EMAIL_USER
        msg["To"] = target_email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        return {"email_status": f"Email sent successfully to {target_email}", "logs": logs}
    except Exception as e:
        return {"email_status": f"Failed to send email: {str(e)}", "logs": logs}