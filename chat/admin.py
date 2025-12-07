from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.AnalysisSession)
class AnalysisSessionAdmin(admin.ModelAdmin):
    # list_display = ('user', 'analysis_type', 'title', 'created_at', 'updated_at', 'is_completed')
    # list_filter = ('analysis_type', 'is_completed', 'created_at')
    # search_fields = ('title',   )
    pass
        
        
@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'is_user', 'timestamp', 'short_content')
    list_filter = ('is_user', 'timestamp')
    search_fields = ('content', 'session__title', 'session__user__username')
    
    def short_content(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    short_content.short_description = 'Content'
    
