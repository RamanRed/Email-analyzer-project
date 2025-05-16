import os
import google.generativeai as genai
import imaplib
import email
from dotenv import load_dotenv
from email.header import decode_header

load_dotenv()
# Load environment variables safely
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")  # Should be your app password
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(GMAIL_USER, GMAIL_PASS, GEMINI_API_KEY)
# Ensure everything is set
if not all([GMAIL_USER, GMAIL_PASS, GEMINI_API_KEY]):
    print("Environment variables not set. Please set GMAIL_USER, GMAIL_PASS, GEMINI_API_KEY.")
    exit()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Connect to Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(GMAIL_USER, GMAIL_PASS)
mail.select("inbox")

# Search for mails from the last 7 days
status, messages = mail.search(None, '(SINCE "09-May-2025")')  # Adjust date as needed

email_ids = messages[0].split()
all_bodies = ""

for eid in email_ids[-10:]:  # Just take the latest 10 mails for demo
    status, msg_data = mail.fetch(eid, "(RFC822)")
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    subject, encoding = decode_header(email_message["subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

    # Extract plain text part
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and part.get("Content-Disposition") is None:
                body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = email_message.get_payload(decode=True).decode(errors="ignore")

    all_bodies += f"\n--- Email ---\nSubject: {subject}\n{body.strip()[:1000]}\n"  # limit size

# Build prompt with email content
prompt = (
    "Below are some cold mails I received this week. "
    "Please summarize them and classify into: "
    "scholarship, internship, placement, college/exams.\n\n"
    + all_bodies
)

# Get summary from Gemini
response = model.generate_content(prompt)
print("\n🧠 Gemini Summary:\n", response.text)
