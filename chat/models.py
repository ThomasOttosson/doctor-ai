from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AnalysisSession(models.Model):
    ANALYSIS_TYPES = [
        ('vitamin_minerals', 'Vitamin & Minerals Intake'),
        ('exercise_routine', 'Weekly Exercise Routine'),
        ('food_quality', 'Weekly Food Quality'),
        ('sleep_quality', 'Sleep Quality & Habits'),
        ('stress_levels', 'Stress Levels & Daily Workload'),
        ('hydration', 'Hydration Levels'),
        ('mental_wellbeing', 'Mental Well-being Routine'),
        ('energy_levels', 'Daily Energy Levels'),
        ('meal_balance', 'Weekly Meal Balance'),
        ('digestion', 'Digestion & Gut Health'),
        ('calorie_intake', 'Daily Calorie Intake'),
        ('posture', 'Posture & Ergonomics'),
        ('exercise_balance', 'Cardio vs Strength Training Balance'),
        ('hormone_health', 'Hormone-supporting Lifestyle'),
        ('immune_health', 'Immune-supporting Habits'),
        ('productivity', 'Daily Productivity & Burnout Risk'),
        ('screen_time', 'Screen Time & Blue-light Exposure'),
        ('environmental_toxins', 'Environmental Toxins Exposure'),
        ('caffeine', 'Caffeine & Stimulant Consumption'),
        ('alcohol', 'Alcohol Intake & Lifestyle Balance'),
        ('menstrual_health', 'Menstrual Cycle Health'),
        ('mobility', 'Daily Mobility & Flexibility'),
        ('chronic_pain', 'Chronic Pain Patterns'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPES)
    title = models.CharField(max_length=200, default="Health Analysis")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_analysis_type_display()}"

class ChatMessage(models.Model):
    session = models.ForeignKey(AnalysisSession, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_user = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{'User' if self.is_user else 'AI'} - {self.content[:50]}"