import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


def send_admin_notification_email(
    request_id: str,
    client_name: str,
    client_phone: str,
    sms_content: Optional[str] = None,
) -> None:
    """
    Envoie un email à l'administrateur pour notifier d'une nouvelle demande de ticket.
    """
    admin_email = os.getenv("ADMIN_EMAIL", "admin@dembeletelecom.com")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    dashbord_url = os.getenv(
        "DASHBOARD_URL", "http://localhost:8000/dashboard")

    # Si les credentials SMTP ne sont pas configurés, on log juste
    if not smtp_user or not smtp_password:
        print(f"[EMAIL] Nouvelle demande de ticket:")
        print(f"  - ID: {request_id}")
        print(f"  - Client: {client_name}")
        print(f"  - Téléphone: {client_phone}")
        print(f"  - SMS: {sms_content}")
        print(f"  - Lien validation: {dashbord_url}")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = admin_email
        msg['Subject'] = f"🔔 Nouvelle demande de ticket - {client_name}"

        body = f"""
        <h2>Nouvelle demande de ticket Wi-Fi</h2>
        
        <p><strong>Client:</strong> {client_name}</p>
        <p><strong>Téléphone:</strong> {client_phone}</p>
        <p><strong>ID Demande:</strong> {request_id}</p>
        
        {f'<p><strong>SMS de confirmation:</strong><br><pre>{sms_content}</pre></p>' if sms_content else ''}
        
        <p>
            <a href="{dashbord_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Voir la demande sur le dashboard
            </a>
        </p>
        """

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print(f"Email envoyé à {admin_email} pour la demande {request_id}")

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        # Fail silently
