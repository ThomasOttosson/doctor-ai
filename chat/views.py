from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
from .models import AnalysisSession, ChatMessage
import uuid

load_dotenv()

# Global storage for guest sessions (in production, use Redis)
guest_sessions = {}

# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            return render(request, 'chat/login.html', {'form': form, 'error': 'Invalid credentials'})
    
    form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'chat/register.html', {'form': form})
    
    form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('chat_interface')

def index(request):
    """Public home page - accessible without login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'chat/index.html')

@login_required
def dashboard(request):
    # Get user's recent sessions
    recent_sessions = AnalysisSession.objects.filter(user=request.user)[:5]
    session_count = AnalysisSession.objects.filter(user=request.user).count()
    
    context = {
        'recent_sessions': recent_sessions,
        'session_count': session_count,
    }
    return render(request, 'chat/dashboard.html', context)

# AI Service
class AIService:
    def __init__(self):
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.model = genai.GenerativeModel('gemini-2.5-pro')
        except:
            try:
                self.model = genai.GenerativeModel('models/gemini-pro')
            except:
                self.model = genai.GenerativeModel('gemini-1.0-pro')
    
    def get_analysis_questions(self, analysis_type):
        analysis_prompts = {
            'vitamin_minerals': """
                You are a medical AI assistant analyzing vitamin and mineral intake.
                Ask specific questions about daily food consumption, fruits and vegetables intake,
                dairy and protein sources, supplement usage, and any deficiency symptoms.
                Ask 3-5 targeted questions to assess potential deficiencies.
            """,
            'exercise_routine': """
                Analyze weekly exercise habits. Ask about types of exercise, frequency, duration,
                intensity levels, recovery practices, and fitness goals.
            """,
            'food_quality': """
                Analyze weekly food quality. Ask about processed vs whole food consumption,
                meal preparation habits, fruit and vegetable variety, and eating patterns.
            """,
            'sleep_quality': """
                Analyze sleep quality and habits. Ask about sleep duration, bedtime routine,
                sleep environment, factors affecting sleep, and energy levels upon waking.
            """,
            'stress_levels': """
                Analyze stress levels and daily workload. Ask about daily stress triggers,
                workload management, coping mechanisms, and work-life balance.
            """,
            'hydration': """
                Analyze hydration levels. Ask about daily water intake, other fluid consumption,
                signs of dehydration, and hydration habits throughout the day.
            """,
            'mental_wellbeing': """
                Analyze mental well-being routine. Ask about daily mood patterns,
                stress management techniques, social connections, and mental health practices.
            """,
            'energy_levels': """
                Analyze daily energy levels. Ask about energy patterns throughout the day,
                factors that boost or drain energy, and impact of sleep and nutrition.
            """,
            'meal_balance': """
                Analyze weekly meal balance. Ask about macronutrient distribution,
                meal timing, food variety, and portion sizes.
            """,
            'digestion': """
                Analyze digestion and gut health. Ask about regular digestion patterns,
                food intolerances, gut symptoms, and fiber intake.
            """,
            'calorie_intake': """
                Analyze daily calorie intake. Ask about typical daily meals, snacking habits,
                beverage calories, and hunger cues.
            """,
            'posture': """
                Analyze posture and ergonomics. Ask about daily sitting/standing patterns,
                workstation setup, and any discomfort or pain.
            """,
            'exercise_balance': """
                Analyze cardio vs strength training balance. Ask about current exercise split,
                fitness goals alignment, and recovery between sessions.
            """,
            'hormone_health': """
                Analyze hormone-supporting lifestyle. Ask about sleep quality, stress management,
                nutrition for hormonal balance, and environmental factors.
            """,
            'immune_health': """
                Analyze immune-supporting habits. Ask about illness frequency, sleep and stress factors,
                nutrition for immunity, and supplement usage.
            """,
            'productivity': """
                Analyze daily productivity and burnout risk. Ask about workload, focus and concentration,
                breaks and recovery, and motivation levels.
            """,
            'screen_time': """
                Analyze screen time and blue-light exposure. Ask about daily screen usage patterns,
                eye comfort, evening screen habits, and blue light protection.
            """,
            'environmental_toxins': """
                Analyze household environmental toxins. Ask about cleaning product types,
                air and water quality, and chemical exposure concerns.
            """,
            'caffeine': """
                Analyze caffeine and stimulant consumption. Ask about daily caffeine sources and amounts,
                timing of consumption, and effects on sleep and energy.
            """,
            'alcohol': """
                Analyze alcohol intake and lifestyle balance. Ask about drinking frequency and quantity,
                social drinking patterns, and effects on sleep and mood.
            """,
            'menstrual_health': """
                Analyze menstrual cycle health. Ask about cycle regularity and symptoms,
                PMS experiences, and impact on daily life.
            """,
            'mobility': """
                Analyze daily mobility and flexibility. Ask about daily movement patterns,
                stretching routine, and joint health.
            """,
            'chronic_pain': """
                Analyze chronic pain or discomfort. Ask about pain locations and patterns,
                triggers and relievers, and impact on daily activities.
            """,
            'default': """
                Ask relevant questions to analyze this health aspect.
                Focus on gathering specific, actionable information.
            """
        }
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts['default'])
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return f"I'll help analyze your {analysis_type.replace('_', ' ')}. Could you tell me more about your current habits and any concerns you have?"

    def clean_basic_markdown(self, text):
        """Remove only problematic markdown, keep useful formatting"""
        import re
        
        # Remove headers but keep the text
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        
        # Remove horizontal rules
        text = re.sub(r'^\s*[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def generate_response(self, conversation_history, analysis_type):
        system_prompt = f"""
        
        You are Doctor AI, a medical AI assistant currently analyzing the user's {analysis_type.replace('_', ' ')}.
        You are having a conversational assessment to gather information.
        
        Instructions:

        Ask only one question at a time to keep the conversation focused.

        Maintain an empathetic, calm, and professional tone.

        Collect specific and actionable information relevant to the user's symptoms, lifestyle, and concerns.

        Continue asking clarifying questions until you have sufficient information to provide a structured overview.

        When enough information has been gathered, offer to give a comprehensive assessment or summary.

        Always remind the user that your responses are informational only and do not replace advice from a licensed healthcare professional.
        
        FORMATTING GUIDELINES:
        - You may use **bold** for emphasis on important terms
        - You may use *italic* for subtle emphasis
        - You may use bullet points with * or -
        - You may use numbered lists
        - DO NOT use headers (#, ##, ###)
        - DO NOT use code blocks (```)
        - DO NOT use horizontal rules (---)
        - Keep formatting minimal and professional
        """
        
        try:
            full_prompt = f"{system_prompt}\n\nConversation history:\n{conversation_history}\n\nYour response:"
            response = self.model.generate_content(full_prompt)
            cleaned_response = self.clean_basic_markdown(response.text)
            return cleaned_response
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "I appreciate you sharing that information. Could you tell me more about your current habits or concerns?"


def chat_interface(request, session_id=None):
    """Main chat interface - accessible to both logged-in and guest users"""
    context = {
        'session_id': session_id,
        'user_authenticated': request.user.is_authenticated,
        'initial_messages': [],
        'session_title': None,
        'analysis_type': None
    }
    
    if session_id and request.user.is_authenticated:
        # Try to load the specific session if provided and user is authenticated
        try:
            session = AnalysisSession.objects.get(id=session_id, user=request.user)
            context['session_title'] = session.title
            context['analysis_type'] = session.analysis_type
            
            # Load messages for this session
            messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
            context['initial_messages'] = [
                {
                    'content': msg.content,
                    'is_user': msg.is_user,
                    'timestamp': msg.timestamp.strftime('%H:%M')
                }
                for msg in messages
            ]
            
            print(f"Loaded session {session_id} for user {request.user.username}")
            # print(f"Initial messages: {context['initial_messages']}")
            
        except AnalysisSession.DoesNotExist:
            # Session doesn't exist or doesn't belong to user
            context['error'] = 'Session not found'
            print(f"Session {session_id} not found for user {request.user.username}")
    
    return render(request, 'chat/chat.html', context)


# API Views - Support both authenticated and guest users
@csrf_exempt
def start_analysis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            analysis_type = data.get('analysis_type')
            
            ai_service = AIService()
            questions = ai_service.get_analysis_questions(analysis_type)
            
            if request.user.is_authenticated:
                # Create database session for logged-in users
                session = AnalysisSession.objects.create(
                    user=request.user,
                    analysis_type=analysis_type,
                    title=f"{analysis_type.replace('_', ' ').title()} Analysis"
                )
                
                # Save AI message to database
                ChatMessage.objects.create(
                    session=session,
                    content=questions,
                    is_user=False
                )
                
                session_id = session.id
                session_type = 'authenticated'
            else:
                # Create in-memory session for guest users
                session_id = str(uuid.uuid4())
                guest_sessions[session_id] = {
                    'analysis_type': analysis_type,
                    'title': f"{analysis_type.replace('_', ' ').title()} Analysis",
                    'messages': [
                        {'content': questions, 'is_user': False, 'timestamp': 'Now'}
                    ],
                    'created_at': 'Just now'
                }
                session_type = 'guest'
            
            return JsonResponse({
                'session_id': session_id,
                'session_type': session_type,
                'ai_response': questions,
                'title': guest_sessions[session_id]['title'] if session_type == 'guest' else f"{analysis_type.replace('_', ' ').title()} Analysis"
            })
            
        except Exception as e:
            print(f"Error in start_analysis: {e}")
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            user_message = data.get('message')
            session_type = data.get('session_type', 'authenticated')
            
            # Save user message
            if session_type == 'authenticated' and request.user.is_authenticated:
                # Authenticated user - save to database
                session = AnalysisSession.objects.get(id=session_id, user=request.user)
                ChatMessage.objects.create(
                    session=session,
                    content=user_message,
                    is_user=True
                )
                
                # Get conversation history from database
                messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
                conversation_history = "\n".join([
                    f"{'User' if msg.is_user else 'Doctor AI'}: {msg.content}" 
                    for msg in messages
                ])
                
                analysis_type = session.analysis_type
                
            else:
                # Guest user - use in-memory storage
                if session_id not in guest_sessions:
                    return JsonResponse({'error': 'Session not found'}, status=404)
                
                guest_sessions[session_id]['messages'].append({
                    'content': user_message,
                    'is_user': True,
                    'timestamp': 'Now'
                })
                
                # Build conversation history from memory
                messages = guest_sessions[session_id]['messages']
                conversation_history = "\n".join([
                    f"{'User' if msg['is_user'] else 'Doctor AI'}: {msg['content']}" 
                    for msg in messages
                ])
                
                analysis_type = guest_sessions[session_id]['analysis_type']
            
            # Get AI response
            ai_service = AIService()
            ai_response = ai_service.generate_response(conversation_history, analysis_type)
            
            # Save AI response
            if session_type == 'authenticated' and request.user.is_authenticated:
                ChatMessage.objects.create(
                    session=session,
                    content=ai_response,
                    is_user=False
                )
                session.save()  # Update timestamp
            else:
                guest_sessions[session_id]['messages'].append({
                    'content': ai_response,
                    'is_user': False,
                    'timestamp': 'Now'
                })
            
            return JsonResponse({'ai_response': ai_response})
            
        except AnalysisSession.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
        except Exception as e:
            print(f"Error in send_message: {e}")
            return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
def get_user_sessions(request):
    """Get all sessions for the current user (authenticated only)"""
    sessions = AnalysisSession.objects.filter(user=request.user).order_by('-updated_at')
    sessions_data = []
    
    for session in sessions:
        sessions_data.append({
            'id': session.id,
            'title': session.title,
            'analysis_type': session.analysis_type,
            'created_at': session.created_at.strftime('%b %d, %Y %H:%M'),
            'message_count': session.messages.count(),
            'is_completed': session.is_completed
        })
    
    return JsonResponse({'sessions': sessions_data})

@login_required
@csrf_exempt
def load_session(request, session_id):
    """Load a specific session and its messages (authenticated only)"""
    try:
        session = AnalysisSession.objects.get(id=session_id, user=request.user)
        messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
        
        messages_data = []
        for message in messages:
            messages_data.append({
                'content': message.content,
                'is_user': message.is_user,
                'timestamp': message.timestamp.strftime('%H:%M')
            })
        
        return JsonResponse({
            'session': {
                'id': session.id,
                'title': session.title,
                'analysis_type': session.analysis_type
            },
            'messages': messages_data
        })
        
    except AnalysisSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)