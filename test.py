from dotenv import load_dotenv
from src.services.email_service import send_admin_notification_email

load_dotenv()


send_admin_notification_email(
    "", "Test User", "+1234567890", "Ceci est un SMS de test.")
