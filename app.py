from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import cohere
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Load your Cohere API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Save all chats to this file
CHAT_LOG_FILE = "chat_history.txt"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    username = data.get('user', 'User')

    try:
        # Simulate delay (handled on frontend) and call Cohere chat
        response = co.chat(message=user_message)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    # Save the chat to file with timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_LOG_FILE, "a") as f:
        f.write(f"[{now}] {username}: {user_message}\n")
        f.write(f"[{now}] Mat BOT: {reply}\n\n")

    return jsonify({"reply": reply})

if __name__ == '__main__':
    print("✅ Mat BOT is running...")
    app.run(debug=True)
