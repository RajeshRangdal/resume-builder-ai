# AI Powered Latex Resume Builder
A comprehensive resume builder tool that helps users create and tailor professional resumes in LaTeX format. Available as both a web application and Chrome extension.

## 🌟 Features
- Create professional LaTeX resumes with a user-friendly interface
- Export resumes in both PDF and DOCX formats
- Tailor resumes to specific job descriptions using AI
- Chrome extension for easy access
- Hosted on Render cloud platform

## 🛠 Technology Stack
- **Backend**: Python
- **Frontend**: HTML, JavaScript
- **AI Integration**: Mistral AI API
- **Document Processing**: LaTeX, python-docx
- **Cloud Platform**: Render

## 📁 Project Structure
```
resume-builder/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── src/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── Tailor_Resume_Tool_v3.py
│   ├── frontend/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── styles.css
│   │   │   └── js/
│   │   │       └── main.js
│   │   ├── templates/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   └── assets/
│   │       └── images/
│   └── chrome-extension/
│       ├── manifest.json
│       ├── popup.html
│       ├── popup.js
│       └── icons/
└── docs/
    ├── CONTRIBUTING.md
    ├── SETUP.md
    └── API.md
```

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8+
- LaTeX installation (TeX Live or MiKTeX)
- Mistral AI API key

### Local Development
1. Clone the repository
```bash
git clone https://github.com/yourusername/resume-builder-ai.git
cd resume-builder-ai
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
export MISTRAL_API_KEY=your_api_key_here
```

5. Run the application
```bash
python src/backend/app.py
```

### Chrome Extension Setup
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable Developer Mode
3. Click "Load unpacked" and select the `src/chrome-extension` directory

## 📝 Usage

### Web Application
1. Navigate to the hosted application or local development server
2. Choose between "Create LaTeX Resume" or "Tailor Resume"
3. Fill in the required information
4. Generate your resume in PDF or DOCX format

### Chrome Extension
1. Click the extension icon in Chrome
2. Fill in your resume details
3. Generate or tailor your resume directly from the browser

## 🔑 API Configuration
Create a `.env` file in the root directory:
```
MISTRAL_API_KEY=your_api_key_here
```

## 🤝 Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## 📄 License
This project is licensed under the Proprietary License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- LaTeX for document formatting
- Mistral AI for resume tailoring capabilities
- Render for hosting services
