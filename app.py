import openai
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("openAI_API_KEY")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    if user_input.lower() == "bye":
        return jsonify({"response": "Bye..."}), 200

    try:
        # Updated API call for the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use chat model like gpt-3.5-turbo or gpt-4
            messages=[
                {"role": "user", "content": user_input}
            ],
            max_tokens=50,
            temperature=0.3
        )

        # Extracting the response from the API
        ai_response = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": ai_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
