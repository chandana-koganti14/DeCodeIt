# DeCodeIt - AI Code Explanation Assistant 🤖

DeCodeIt is an interactive AI-powered code explanation assistant that helps developers understand code snippets by providing detailed explanations, dry runs, similar coding questions, and fun facts. Built with **Flask (Python)** and **Google's Generative AI model**, it offers a user-friendly interface for both beginners and experienced developers.

---

## Features ✨

- **Code Explanation**: Provides a step-by-step breakdown of any code snippet.
- **Dry Run**: Demonstrates how the code executes with example inputs.
- **Similar Coding Questions**: Suggests related coding problems for practice.
- **Fun Facts**: Shares interesting programming-related trivia.
- **Follow-Up Questions**: Allows users to ask additional questions about the code.
- **Interactive UI**: Clean and intuitive web interface with animations.

---

## Technologies Used 🛠️

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **AI Model**: Google Generative AI (`gemini-2.0-flash`)
- **Environment Management**: `dotenv`
- **Version Control**: Git

---

## Setup Instructions 🚀

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/DeCodeIt.git
cd DeCodeIt
```

### 2. Extract Specific Cell Types

```bash
GEMINI_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
python app.py
```
The application will start running at http://127.0.0.1:5000/. Open this URL in your browser to access the DeCodeIt interface.

## Project Structure 📂
```plaintext
DeCodeIt/
├── app.py                  # Flask backend and AI integration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API key)
├── static/                 # Static files (CSS, images, etc.)
│   └── images/             # GIFs and other images
├── templates/              # HTML templates
│   └── index.html          # Main frontend interface
├── README.md               # Project documentation
└── .gitignore              # Files to ignore in Git
```

## Usage 🖥️

Enter Code: Paste your code snippet into the text area.

Explain Code: Click the "Explain Code" button to generate a detailed explanation.

Follow-Up: Ask additional questions using the follow-up section.

Explore: View the dry run, similar coding questions, and fun facts.
