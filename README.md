# D Learning Test Generator

A modern web application for generating and taking computer science tests using AI.

## Features

- Beautiful, responsive homepage with navigation
- AI-powered test generation based on user requests
- Interactive test-taking interface
- Detailed progress dashboard
- AI-powered feedback system

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Gemini API key. You can
   copy `.env.example` as a starting point:
```
GEMINI_API_KEY=your_api_key_here
```

Create the key in [Google AI Studio](https://aistudio.google.com/app/apikey).
Use an API key, not an OAuth access token or service-account credential. Keep
the key private; do not commit it or share it. The application reads `.env`
(not `.env.txt`). Restart the Django server after changing `.env`. Test and
revision-note generation both require a valid Gemini API key.

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

- `core/` - Main Django project settings
- `quiz/` - Quiz application
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images) 