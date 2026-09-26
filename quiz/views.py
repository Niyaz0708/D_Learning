from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages
from django.urls import reverse
from .models import Category, Test, Question, UserResponse
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import logging
import json
import re
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Configure Gemini
api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
model = "gemini-3.5-flash-lite"
client = None

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        logger.info("Gemini model configured successfully")
    except Exception:
        logger.exception("Error configuring Gemini")
else:
    logger.warning(
        "Gemini is not configured. Add GEMINI_API_KEY to the project .env file "
        "before generating tests."
    )

def clean_json_response(text):
    """Clean the response text by removing markdown code blocks and any other non-JSON content."""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Remove any leading/trailing whitespace
    text = text.strip()
    
    logger.info(f"Cleaned JSON text: {text[:100]}...")
    return text

def gemini_authentication_help(error):
    """Return actionable setup guidance for rejected Gemini credentials."""
    error_text = str(error).upper()
    if '401' not in error_text and 'UNAUTHENTICATED' not in error_text:
        return None

    return (
        'Google rejected the Gemini credentials. Replace GEMINI_API_KEY in the '
        'project-root .env file with a valid Google AI Studio API key (not an '
        'OAuth access token), then restart the Django server. Create a key at '
        'https://aistudio.google.com/app/apikey. Do not share the key.'
    )

@login_required
def home(request):
    categories = Category.objects.all()
    recent_tests = Test.objects.filter(user=request.user).order_by('-date_created')[:4] if request.user.is_authenticated else None
    
    context = {
        'categories': categories,
        'recent_tests': recent_tests,
    }
    return render(request, 'quiz/home.html', context)

@login_required
@require_POST
def quick_revision(request):
    category_id = request.POST.get('category')
    topic = request.POST.get('topic', '').strip()
    home_url = f"{reverse('quiz:home')}#quick-revision"

    try:
        category = Category.objects.get(id=category_id)
    except (Category.DoesNotExist, ValueError, TypeError):
        messages.error(request, 'Please choose a valid subject for your revision notes.')
        return redirect(home_url)

    if not topic:
        messages.error(request, 'Please enter a topic for your revision notes.')
        return redirect(home_url)

    if not client:
        messages.error(
            request,
            'Revision notes are unavailable because the Gemini API key is not configured.',
        )
        return redirect(home_url)

    prompt = f"""
Create concise, accurate exam revision notes for the subject "{category.name}" and topic "{topic}".
Write in plain text using short headings and bullet points. Include:
- A brief overview and essential definitions
- The most important concepts or steps to remember
- One simple example or application
- Common exam mistakes to avoid
- Three quick self-check questions with short answers
Keep the notes focused and under 500 words. Do not invent facts.
"""

    try:
        response = client.models.generate_content(model=model, contents=prompt)
        notes = (response.text or '').strip()
        if not notes:
            raise ValueError('The notes service returned an empty response.')
    except Exception as exc:
        logger.exception('Error generating revision notes for %s: %s', category.name, topic)
        messages.error(
            request,
            gemini_authentication_help(exc)
            or 'We could not create revision notes right now. Please try again.',
        )
        return redirect(home_url)

    return render(request, 'quiz/revision_notes.html', {
        'category': category,
        'topic': topic,
        'notes': notes,
    })

def generate_questions_for_test(test, num_questions):
    """Generate questions for a test using the Gemini AI model."""
    if not client:
        error_msg = (
            "Gemini API key is missing. Add GEMINI_API_KEY=your_key_here "
            "to a .env file in the project root, then restart the server."
        )
        logger.error(error_msg)
        raise Exception(error_msg)

    logger.info(f"Generating {num_questions} questions for test {test.id}")
    
    # Generate test using Gemini
    prompt = f"""
    Generate {num_questions} multiple-choice questions about {test.topic} in the field of {test.category.name} at {test.difficulty} level.
    For each question, provide:
    1. The question text
    2. Four options (A, B, C, D)
    3. The correct answer (A, B, C, or D)
    4. A detailed explanation of why the answer is correct

    Format each question as a JSON object with the following structure:
    {{
        "question": "question text",
        "options": {{
            "A": "option A",
            "B": "option B",
            "C": "option C",
            "D": "option D"
        }},
        "correct_answer": "A",
        "explanation": "Detailed explanation of why this is the correct answer"
    }}

    Return all questions as a JSON array. Do not include any markdown formatting or code blocks.
    Only return the raw JSON array.
    """

    try:
        # Generate content with Gemini
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        
        logger.info(f"Received response from Gemini for test {test.id}")
        
        # Clean and parse the JSON response
        cleaned_response = clean_json_response(response.text)
        questions_data = json.loads(cleaned_response)
        
        if not questions_data:
            raise Exception("No questions were generated")
            
        logger.info(f"Successfully parsed {len(questions_data)} questions for test {test.id}")
        
        # Create questions
        for q_data in questions_data:
            Question.objects.create(
                test=test,
                text=q_data['question'],
                options=q_data['options'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation']
            )
        
        logger.info(f"Created {len(questions_data)} questions for test {test.id}")
        
    except Exception as e:
        logger.error(f"Error generating questions for test {test.id}: {str(e)}")
        # Delete the test if question generation failed
        test.delete()
        raise Exception(f"Failed to generate questions: {str(e)}")

@login_required
def generate_test(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        num_questions = request.POST.get('num_questions', 10)
        time_limit = request.POST.get('time_limit', 30)
        
        try:
            category = Category.objects.get(id=category_id)
            
            # Create the test
            test = Test.objects.create(
                user=request.user,
                category=category,
                topic=topic,
                difficulty=difficulty,
                time_limit=time_limit
            )
            
            # Generate questions using AI
            generate_questions_for_test(test, int(num_questions))
            
            return redirect('quiz:take_test', test_id=test.id)
            
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category selected.')
        except Exception as e:
            messages.error(
                request,
                gemini_authentication_help(e) or f'Error generating test: {str(e)}',
            )
            logger.error(f'Error generating test: {str(e)}')
    
    context = {
        'categories': categories
    }
    return render(request, 'quiz/generate_test.html', context)

@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, user=request.user)
    questions = test.questions.all()
    
    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        user_responses = []
        
        for question in questions:
            answer = request.POST.get(f'answer_{question.id}')
            if answer:
                is_correct = answer.upper() == question.correct_answer
                if is_correct:
                    score += 1
                
                response = UserResponse.objects.create(
                    question=question,
                    user=request.user,
                    answer=answer,
                    is_correct=is_correct
                )
                user_responses.append(response)
        
        # Calculate final score
        test.score = (score / total_questions) * 100
        test.save()
        
        # Render results page
        return render(request, 'quiz/test_results.html', {
            'test': test,
            'user_responses': user_responses,
            'correct_answers': score,
            'incorrect_answers': total_questions - score,
        })
    
    # Prepare questions with options for the template
    questions_with_options = []
    for question in questions:
        questions_with_options.append({
            'id': question.id,
            'text': question.text,
            'options': question.options
        })
    
    return render(request, 'quiz/take_test.html', {
        'test': test,
        'questions': questions_with_options
    })

@login_required
def dashboard(request):
    # Get user's tests
    tests = Test.objects.filter(user=request.user).order_by('-date_created')
    
    # Calculate overall progress
    total_tests = tests.count()
    completed_tests = [test for test in tests if test.score is not None]
    if completed_tests:
        overall_progress = sum(test.score for test in completed_tests) / len(completed_tests)
    else:
        overall_progress = 0
    
    # Get recent tests (last 5)
    recent_tests = tests[:5]
    
    # Calculate category scores
    category_scores = {}
    for test in tests:
        if test.score is not None:  # Only include tests with scores
            if test.category not in category_scores:
                category_scores[test.category] = []
            category_scores[test.category].append(test.score)
    
    # Calculate average score for each category
    for category in category_scores:
        scores = [s for s in category_scores[category] if s is not None]
        if scores:
            category_scores[category] = sum(scores) / len(scores)
        else:
            category_scores[category] = 0
    
    return render(request, 'quiz/dashboard.html', {
        'overall_progress': overall_progress,
        'total_tests': total_tests,
        'recent_tests': recent_tests,
        'category_scores': category_scores
    })

def about(request):
    categories = Category.objects.all()
    return render(request, 'quiz/about.html', {'categories': categories})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
