from flask import Flask, request, jsonify, render_template
from google.generativeai import GenerativeModel
import os
from dotenv import load_dotenv
import re  # For cleaning up the response

# Load environment variables (API key)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Model configuration
MODEL_NAME = "gemini-2.0-flash"  # Use the correct model name

# Configure the API key
genai_api_key = os.getenv("GEMINI_API_KEY")
if not genai_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

# Initialize the GenerativeModel
model = GenerativeModel(MODEL_NAME)

# Conversation history storage (in-memory for simplicity)
conversation_history = {}

# Function to generate a response from the AI model
def get_ai_response(conversation_id, user_input):
    # Retrieve conversation history
    history = conversation_history.get(conversation_id, [])
    
    # Append the latest user input
    history.append({"role": "user", "content": user_input})
    
    # Generate AI response
    content = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
    try:
        # Generate content
        response = model.generate_content(
            content,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 20,
                "candidate_count": 1,
                "max_output_tokens": 3000,
            },
        )
        if response and response.text:
            ai_response = response.text.strip()
            # Append AI response to history
            history.append({"role": "assistant", "content": ai_response})
            # Update conversation history
            conversation_history[conversation_id] = history
            return ai_response
        return "Error: No response generated"
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to clean up the AI-generated response
def clean_response(text):
    """
    Cleans up the AI-generated response by removing unwanted formatting.
    """
    # Remove unwanted characters like ''' and ***
    text = re.sub(r"'''", '', text)  # Remove triple quotes
    text = re.sub(r'\*+', '', text)  # Remove asterisks
    text = re.sub(r'\n+', '\n', text).strip()  # Remove extra newlines
    return text

# Default route to serve the front-end
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# API endpoint for initial code explanation
@app.route('/explain-code', methods=['POST'])
def explain_code():
    data = request.json
    conversation_id = data.get('conversation_id')
    code_snippet = data.get('code')
    
    if not conversation_id or not code_snippet:
        return jsonify({"error": "Both conversation_id and code are required"}), 400
    
    # Generate initial explanation
    prompt = f"""
    Explain this code step by step in a structured format:
    1. Summary: Briefly describe what the code does.
    2. Dry Run: Show how the code executes with an example input.
    3. Similar Coding Questions: Provide 3 similar coding questions related to this code.
    4. Fun Fact: Include a fun fact about programming related to this code.
    Code to explain:
    {code_snippet}
    """
    explanation = get_ai_response(conversation_id, prompt)
    
    # Clean up the response
    cleaned_explanation = clean_response(explanation)
    
    # Debugging: Log the cleaned explanation
    print("Cleaned Explanation:", cleaned_explanation)
    
    return jsonify({"explanation": cleaned_explanation}), 200

# API endpoint for follow-up questions
@app.route('/follow-up', methods=['POST'])
def follow_up():
    data = request.json
    conversation_id = data.get('conversation_id')
    question = data.get('question')
    
    if not conversation_id or not question:
        return jsonify({"error": "Both conversation_id and question are required"}), 400
    
    # Generate follow-up response
    response = get_ai_response(conversation_id, question)
    
    # Clean up the response
    cleaned_response = clean_response(response)
    
    return jsonify({"response": cleaned_response}), 200

if __name__ == '__main__':
    app.run(debug=True)