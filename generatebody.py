import os
import imaplib
import email
from dotenv import load_dotenv
from email.header import decode_header
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")  # Use app password
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not all([GMAIL_USER, GMAIL_PASS, GEMINI_API_KEY]):
    print("❌ Missing environment variables: GMAIL_USER, GMAIL_PASS, or GEMINI_API_KEY.")
    exit()

# --- Configure Gemini API ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# --- Connect to Gmail ---
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(GMAIL_USER, GMAIL_PASS)
mail.select("inbox")

# --- Fetch emails ---
status, messages = mail.search(None, '(SINCE "09-May-2025")')
email_ids = messages[0].split()
listmails = []
all_bodies = ""

for eid in email_ids[-10:]:  # Limit to 10 latest emails
    status, msg_data = mail.fetch(eid, "(RFC822)")
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Decode subject
    subject, encoding = decode_header(email_message["subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

    # Extract plain text body
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = email_message.get_payload(decode=True).decode(errors="ignore")

    mail_dic = {subject: body}
    listmails.append(mail_dic)
    all_bodies += f"\n--- Email ---\nSubject: {subject}\n{body.strip()[:1000]}\n"

# --- Build prompt ---
prompt = (
    """
    Given the following emails, classify each email into relevant categories based on its content.

Output a valid Python dictionary only.

The dictionary should follow this structure:
{
  "Category Name 1": [list of email indices],
  "Category Name 2": [list of email indices],
  ...
}

Notes:
- Indexing starts from 0.
- An email can belong to multiple categories.
- Create new categories as needed.
- Include an "Others" category if some emails do not fit into any defined group.
- Do not add any explanation or extra formatting—just return the dictionary.

Here are the emails:
{all_bodies}

    """
)



# --- Parse Gemini response to dictionary ---
import ast

import ast
import re

def parse_gemini_dict(response_text):
    try:
        # Extract content between triple backticks using regex
        match = re.search(r"```(?:python)?\s*({.*?})\s*```", response_text, re.DOTALL)
        if not match:
            print("❌ Could not find a valid dictionary block inside triple backticks.")
            return {}
        
        dict_str = match.group(1)

        # Parse safely
        parsed_dict = ast.literal_eval(dict_str)

        # Clean and validate the output
        clean_map = {}
        for key, value in parsed_dict.items():
            if isinstance(key, str) and isinstance(value, list):
                clean_map[key.strip()] = [int(i) for i in value if isinstance(i, int)]
        return clean_map

    except Exception as e:
        print(f"❌ Error parsing Gemini dictionary: {e}")
        return {}

# --- Menu functions ---
def show_menu():
    print("\n----- Email Assistant Menu -----")
    print("1. View categories and associated emails")
    print("2. Read emails from a category")
    print("3. Reply to a specific email")
    print("4. Exit")

def view_categories(category_map):
    print("\n📂 Categories and Email Indices:")
    for cat, indices in category_map.items():
        print(f"{cat}: {indices}")

def read_emails(category_map, listmails):
    # print(category_map)
    # print(listmails)
    cat = input("\nEnter category name to read emails: ").strip()
    if cat not in category_map:
        print("❌ Invalid category!")
        return
    for i in category_map[cat]:
        print(f"index of mail : {i} \n ")
        mail = listmails[i]
        subject = next(iter(mail))
        body = mail[subject]
        print(f"\n📧 Email {i}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")

def reply_email(listmails):
    try:
        idx = int(input("\nEnter the index of the email to reply to: "))
        if 0 <= idx < len(listmails):
            #listmails givea dictinory and iter gives the list of key in dictionary then next function retreives the first/ 0th index key
            subject = next(iter(listmails[idx]))
            # storing the body of mail
            body=listmails[idx][subject]
            # here i will initate the langchain function to reply
            print(f"\n📤 Replying to: {subject}")
            reply = input("Enter your reply message: ")
            print(f"\n✅ Simulated reply sent:\n{reply}")
        else:
            print("❌ Invalid index.")
    except ValueError:
        print("❌ Please enter a valid number.")



# --- Ask Gemini for category mapping ---
response = model.generate_content(prompt)
response_text = response.text  # The raw Gemini output as a string
category_map = parse_gemini_dict(response_text)

# Now you can use category_map like:
print(category_map.keys())  # List of categories



print("\n🧠 Gemini Categorization:\n", response_text)


# --- Main loop ---
while True:
    show_menu()
    choice = input("Choose an option (1-4): ")
    if choice == "1":
        view_categories(category_map)
    elif choice == "2":
        read_emails(category_map, listmails)
    elif choice == "3":
        reply_email(listmails)
    elif choice == "4":
        print("👋 Exiting... Goodbye!")
        break
    else:
        print("❌ Invalid choice. Please select from the menu.")
