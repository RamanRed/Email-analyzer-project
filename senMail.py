import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
#turn on vpn to work with it
# Load environment variables
load_dotenv()

# Email configuration
sender_mail = "ramanrandive2004@gmail.com"  # Must be Gmail
receiver_mail = "ramanrandive2004@gmail.com"
sender_password = os.getenv("SENDER_MAIL_PASSWORD")  # Gmail App Password

# Create the email message
msg = MIMEMultipart()
msg["From"] = sender_mail
msg["To"] = receiver_mail
msg["Subject"] = "Testing mails, no worries"

body = "This is a test email for trial purposes. Thank you, Raman!!!"
msg.attach(MIMEText(body, "plain"))

# Send the email
server = None
try:
    # Use SMTP_SSL on port 465
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
    server.login(sender_mail, sender_password)
    server.sendmail(sender_mail, receiver_mail, msg.as_string())
    print("Mail sent successfully")
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication failed: {e}")
except TimeoutError as e:
    print(f"Connection timed out: {e}")
except Exception as e:
    print(f"Error occurred while sending mail: {e}")
finally:
    if server is not None:
        server.quit()