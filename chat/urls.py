from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Main pages
    # path('', views.index, name='index'),  # Public home page
    path('chat/', views.chat_interface, name='chat_interface'),
    path('chat/<int:session_id>/', views.chat_interface, name='chat_session'),  # FIXED: Added name
    
    # API URLs - Make sure these match your frontend calls
    path('api/start_analysis/', views.start_analysis, name='start_analysis'),
    path('api/send_message/', views.send_message, name='send_message'),
    path('api/sessions/', views.get_user_sessions, name='get_sessions'),
    path('api/sessions/<int:session_id>/', views.load_session, name='load_session'),
]