# this llm is stuck due to biling accounf of gemini 


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def generate_email_reply(subject: str, body: str):
    # Initialize LLM and conversation chain with memory
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(llm=llm, memory=memory)

    print("Email Reply Assistant (type 'exit' to quit)\n")

    while True:
        # Get user input for intent and tone
        user_intent = input("Enter user intent as the reply to the mail:\n")
        if user_intent.lower() == "exit":
            print("Exiting email reply assistant.")
            break

        tone = input("""
            Choose the tone of the reply from the following options:
            - Formal
            - Friendly
            - Concise
            - Appreciative
            - Exit to close reply

            Enter your choice:\n""").strip()
        if tone.lower() == "exit":
            print("Exiting email reply assistant.")
            break

        # Format prompt with current inputs
        prompt = f"""
            You are an email assistant helping users write professional, polite, and context-aware replies to incoming emails.

            Given the original email content and the user's intent, generate a clear and concise reply.

            ---

            Original Email:
            Subject: {subject}
            Body: {body}

            User's Intent (what the user wants to say):
            {user_intent}

            Tone: {tone} (e.g., Formal, Friendly, Concise, Appreciative)

            ---

            Generate the reply email in the appropriate tone. Begin with a greeting, address the sender appropriately, and end with a suitable closing. Avoid repeating information unnecessarily.

            Only generate the email body. Do not include subject lines or metadata.
        """

        # Call the conversation chain
        response = conversation.predict(input=prompt)

        print("\nGenerated Reply:\n")
        print(response)
        print("\n" + "="*50 + "\n")


# Example usage:
# if __name__ == "__main__":
#     # Example subject and body coming from elsewhere
#     # example_subject = "Project Deadline Update"
#     # example_body = "Hi Raman, the deadline for the project submission has been moved to next Friday. Please confirm if you need any assistance."

#     generate_email_reply(subject, body)
