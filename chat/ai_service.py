import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        # Configure Gemini with correct API version
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # # Get available models to verify
        # try:
        #     available_models = genai.list_models()
        #     print("Available models:")
        #     for model in available_models:
        #         print(f"- {model.name}")
        # except Exception as e:
        #     print(f"Error listing models: {e}")
    
    def get_model(self):
        """Get the correct Gemini model"""
        try:
            # Try the newer model names
            return genai.GenerativeModel('gemini-2.5-pro')
        except:
            try:
                # Fallback to other possible model names
                return genai.GenerativeModel('models/gemini-pro')
            except:
                # Last fallback
                return genai.GenerativeModel('gemini-pro')
    
    def get_analysis_questions(self, analysis_type, user_context=""):
        """Generate questions for specific analysis types using Gemini"""
        
        analysis_prompts = {
            'vitamin_minerals': """
                You are a medical AI assistant analyzing vitamin and mineral intake.
                Ask specific questions about:
                - Daily food consumption patterns
                - Fruits and vegetables intake frequency
                - Dairy, meat, and plant-based protein sources
                - Supplement usage and types
                - Any deficiency symptoms like fatigue, skin issues, or hair problems
                - Dietary restrictions or preferences
                
                Ask 3-5 targeted, conversational questions to assess potential vitamin/mineral deficiencies.
                Be empathetic and professional.
            """,
            'exercise_routine': """
                Analyze weekly exercise habits. Ask about:
                - Types of exercise (cardio, strength, flexibility)
                - Frequency (days per week) and duration
                - Intensity levels and progression
                - Recovery practices and rest days
                - Fitness goals and current challenges
                - Any pain or discomfort during/after exercise
            """,
            'food_quality': """
                Analyze weekly food quality. Ask about:
                - Processed vs whole food consumption
                - Meal preparation habits
                - Fruit and vegetable variety and quantity
                - Healthy fat sources
                - Sugar and salt intake
                - Eating patterns and timing
            """,
            'sleep_quality': """
                Analyze sleep quality and habits. Ask about:
                - Sleep duration and consistency
                - Bedtime routine
                - Sleep environment factors
                - Factors affecting sleep (caffeine, stress, etc.)
                - Energy levels upon waking
                - Sleep tracking if any
            """,
            'stress_levels': """
                Analyze stress levels and daily workload. Ask about:
                - Daily stress triggers and sources
                - Workload and time management
                - Coping mechanisms
                - Work-life balance
                - Physical symptoms of stress
                - Relaxation practices
            """,
            'hydration': """
                Analyze hydration levels. Ask about:
                - Daily water intake and sources
                - Other fluid consumption
                - Signs of dehydration
                - Factors affecting hydration needs
                - Hydration habits throughout the day
            """,
            'mental_wellbeing': """
                Analyze mental well-being routine. Ask about:
                - Daily mood patterns
                - Stress management techniques
                - Social connections and support
                - Hobbies and leisure activities
                - Mental health practices
                - Work satisfaction
            """,
            'energy_levels': """
                Analyze daily energy levels. Ask about:
                - Energy patterns throughout the day
                - Factors that boost or drain energy
                - Sleep quality impact
                - Nutrition's effect on energy
                - Exercise impact on energy
            """,
            'meal_balance': """
                Analyze weekly meal balance. Ask about:
                - Macronutrient distribution
                - Meal timing and frequency
                - Food variety across the week
                - Portion sizes
                - Snacking habits
            """,
            'digestion': """
                Analyze digestion and gut health. Ask about:
                - Regular digestion patterns
                - Food intolerances or sensitivities
                - Gut symptoms (bloating, gas, etc.)
                - Fiber intake
                - Probiotic food consumption
            """,
            'calorie_intake': """
                Analyze daily calorie intake. Ask about:
                - Typical daily meals and portions
                - Snacking habits
                - Beverage calories
                - Hunger and fullness cues
                - Weight management goals
            """,
            'posture': """
                Analyze posture and ergonomics. Ask about:
                - Daily sitting/standing patterns
                - Workstation setup
                - Posture awareness
                - Any discomfort or pain
                - Movement breaks frequency
            """,
            'exercise_balance': """
                Analyze cardio vs strength training balance. Ask about:
                - Current exercise split
                - Fitness goals alignment
                - Recovery between sessions
                - Performance progression
            """,
            'hormone_health': """
                Analyze hormone-supporting lifestyle. Ask about:
                - Sleep quality and patterns
                - Stress management
                - Nutrition for hormonal balance
                - Environmental factors
                - Energy and mood patterns
            """,
            'immune_health': """
                Analyze immune-supporting habits. Ask about:
                - Illness frequency and recovery
                - Sleep and stress factors
                - Nutrition for immunity
                - Supplement usage
                - Lifestyle factors affecting immunity
            """,
            'productivity': """
                Analyze daily productivity and burnout risk. Ask about:
                - Workload and deadlines
                - Focus and concentration
                - Breaks and recovery
                - Motivation levels
                - Work satisfaction
            """,
            'screen_time': """
                Analyze screen time and blue-light exposure. Ask about:
                - Daily screen usage patterns
                - Eye comfort and strain
                - Evening screen habits
                - Blue light protection measures
                - Digital detox practices
            """,
            'environmental_toxins': """
                Analyze household environmental toxins. Ask about:
                - Cleaning product types
                - Air and water quality
                - Plastic usage
                - Home ventilation
                - Chemical exposure concerns
            """,
            'caffeine': """
                Analyze caffeine and stimulant consumption. Ask about:
                - Daily caffeine sources and amounts
                - Timing of consumption
                - Effects on sleep and energy
                - Dependency feelings
                - Alternative energy sources
            """,
            'alcohol': """
                Analyze alcohol intake and lifestyle balance. Ask about:
                - Drinking frequency and quantity
                - Social drinking patterns
                - Effects on sleep and mood
                - Health concerns
                - Balance with other lifestyle factors
            """,
            'menstrual_health': """
                Analyze menstrual cycle health. Ask about:
                - Cycle regularity and symptoms
                - PMS experiences
                - Impact on daily life
                - Management strategies
                - Hormonal concerns
            """,
            'mobility': """
                Analyze daily mobility and flexibility. Ask about:
                - Daily movement patterns
                - Stretching routine
                - Joint health and stiffness
                - Mobility limitations
                - Exercise variety
            """,
            'chronic_pain': """
                Analyze chronic pain or discomfort. Ask about:
                - Pain locations and patterns
                - Triggers and relievers
                - Impact on daily activities
                - Management strategies
                - Professional consultations
            """,
            'default': """
                Ask relevant questions to analyze this health aspect.
                Focus on gathering specific, actionable information in a conversational way.
            """
        }
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts['default'])
        
        try:
            # Get the correct model
            model = self.get_model()
            
            # Generate content with Gemini
            response = model.generate_content(
                f"{prompt}\n\nUser context: {user_context}\n\nPlease provide 3-5 specific questions to start the conversation:"
            )
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            # Fallback response
            fallback_questions = {
                'vitamin_minerals': "To understand your vitamin and mineral intake, could you tell me about your typical daily meals and any supplements you take?",
                'exercise_routine': "Let's start by understanding your current exercise routine. What types of physical activity do you typically do each week?",
                'food_quality': "I'd like to learn about your eating habits. What does a typical day of meals look like for you?",
                'sleep_quality': "Let's discuss your sleep patterns. How many hours do you usually sleep and what's your bedtime routine like?",
                'stress_levels': "To understand your stress levels, could you describe a typical workday and how you manage daily pressures?",
                'hydration': "Let's talk about your hydration habits. How much water do you typically drink in a day?",
                'mental_wellbeing': "I'd like to understand your mental wellbeing. How have you been feeling emotionally lately?",
                'energy_levels': "Let's discuss your energy patterns. When during the day do you feel most and least energetic?",
                'meal_balance': "To analyze your meal balance, could you describe what you typically eat for breakfast, lunch, and dinner?",
                'digestion': "I'd like to understand your digestive health. How would you describe your typical digestion patterns?",
                'calorie_intake': "Let's talk about your food intake. What does a typical day of eating look like for you?",
                'posture': "To understand your posture habits, could you describe your typical work setup and how you sit during the day?",
                'exercise_balance': "Let's discuss your exercise routine. What's the balance between cardio and strength training in your week?",
                'hormone_health': "I'd like to understand factors affecting your hormonal balance. How would you describe your sleep and stress levels?",
                'immune_health': "Let's talk about your immune health. How often do you get sick and how quickly do you recover?",
                'productivity': "To understand your productivity patterns, could you describe a typical workday and how you manage your tasks?",
                'screen_time': "Let's discuss your screen usage. How many hours per day do you typically spend looking at screens?",
                'environmental_toxins': "I'd like to understand your environmental exposures. What types of cleaning products do you use at home?",
                'caffeine': "Let's talk about your caffeine intake. How much coffee, tea, or other caffeinated drinks do you consume daily?",
                'alcohol': "To understand your alcohol consumption, how often do you typically drink alcoholic beverages?",
                'menstrual_health': "I'd like to understand your menstrual cycle. How regular are your periods and what symptoms do you experience?",
                'mobility': "Let's discuss your mobility. How often do you stretch or do flexibility exercises?",
                'chronic_pain': "I'd like to understand any discomfort you experience. Where do you feel pain and how does it affect your daily life?"
            }
            return fallback_questions.get(analysis_type, f"I'll help analyze your {analysis_type.replace('_', ' ')}. Could you tell me more about your current habits and any concerns you have?")

    def generate_analysis_report(self, analysis_type, user_responses):
        """Generate final analysis based on user responses using Gemini"""
        
        prompt = f"""
        Based on the following conversation about the user's {analysis_type.replace('_', ' ')},
        provide a comprehensive analysis with:
        
        1. KEY OBSERVATIONS: Summarize the main patterns and findings
        2. AREAS FOR IMPROVEMENT: Specific, actionable suggestions
        3. RECOMMENDATIONS: Practical steps the user can take
        4. PROFESSIONAL GUIDANCE: When to consult healthcare professionals
        
        Keep the tone professional, empathetic, and encouraging.
        
        Conversation context: {user_responses}
        
        Please structure your response clearly with headings for each section.
        """
        
        try:
            model = self.get_model()
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return f"Based on our conversation, I recommend focusing on balanced {analysis_type.replace('_', ' ')} habits. Consider consulting with a healthcare provider for personalized advice tailored to your specific situation."

    def chat_response(self, conversation_history, analysis_type):
        """Generate contextual chat responses using Gemini"""
        
        system_prompt = f"""
        You are Doctor AI, a medical AI assistant currently analyzing the user's {analysis_type.replace('_', ' ')}.
        You are having a conversational assessment to gather information.
        
        Guidelines:
        - Ask one question at a time to keep the conversation focused
        - Be empathetic and professional
        - Gather specific, actionable information
        - When you have enough information, offer to provide a comprehensive analysis
        - Always remind users to consult healthcare professionals for medical advice
        - Keep responses conversational and natural
        """
        
        try:
            model = self.get_model()
            full_prompt = f"{system_prompt}\n\nConversation history:\n{conversation_history}\n\nYour response:"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "I appreciate you sharing that information. Could you tell me more about your current habits or concerns?"