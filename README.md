✉️ AI-Powered Email Categorizer (CLI)
A Python-based command-line tool that fetches your latest emails, uses a Generative AI model (e.g., Gemini) to categorize them, and allows you to view, read, or reply to emails based on categories.

🔧 Features
✅ Fetches your 10 latest emails via IMAP

🤖 Uses Gemini LLM via LangChain to generate intelligent email categories

📂 Supports multiple categories like Promotions, Travel, Updates, etc.

🧠 Handles emails with multiple categories using index-based tracking

📬 Enables users to read or reply to categorized emails via CLI

🔒 Loads sensitive credentials from .env for safety

📦 Requirements
Install the following Python packages:

bash
Copy
Edit
pip install langchain langchain-google-genai python-dotenv google-generativeai
The script uses:

python
Copy
Edit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
🚀 How to Run
Configure your .env file with required keys and credentials:

ini
Copy
Edit
GOOGLE_API_KEY=your-api-key
EMAIL=your-email
APP_PASSWORD=your-app-password
Run the CLI tool:

bash
Copy
Edit
python generatebody.py
Follow the on-screen menu:

pgsql
Copy
Edit
1. View categories and associated emails
2. Read emails from a category
3. Reply to a specific email
4. Exit
🧠 Prompt Structure to Gemini
Emails are sent to the LLM using this format:

python
Copy
Edit
{
  "Category Name 1": [indices],
  "Category Name 2": [indices],
  ...
}
The model returns only a valid Python dictionary — no extra text.

📌 Notes
Email indices begin at 0

Handles multi-category classification

Prevents index out-of-range errors

Categorization is fully AI-driven and dynamically adapts to content
