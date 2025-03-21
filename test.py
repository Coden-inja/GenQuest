from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual DeepSeek API Key
API_KEY = "your_deepseek_api_key"
DEEPSEEK_URL = "https://api.deepseek.com/v1/completions"  # Adjust if needed

@app.route("/")
def index():
    return render_template("templates/test.html")

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    prompt = data.get("prompt", "")

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
    result = response.json()

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
