# Doctor AI - AI Medical Assistant

## 📋 Overview

Doctor AI is a comprehensive AI-powered medical assistant application that provides personalized health analysis through intelligent conversations. Built with Django, this application offers a responsive web interface for users to analyze various aspects of their health and wellness.

## ✨ Features

### 🏥 Health Analysis Categories
- **Nutrition & Diet**: Vitamin/mineral intake, food quality, meal balance, calorie tracking, digestion analysis
- **Exercise & Fitness**: Workout routines, cardio vs strength balance, mobility, posture assessment
- **Mental Health & Wellness**: Sleep quality, stress levels, mental wellbeing, energy tracking, productivity
- **Lifestyle & Habits**: Hydration, caffeine/alcohol consumption, screen time analysis
- **Health & Wellness**: Hormone health, immune system, chronic pain, environmental toxins, menstrual health

### 💻 User Features
- **Responsive Chat Interface**: Clean, modern chat UI with markdown support
- **Session Management**: Save and continue previous health conversations
- **User Authentication**: Secure login/registration system
- **Dashboard**: Overview of health statistics and recent analyses
- **Mobile Responsive**: Fully functional on all device sizes

## 🛠️ Technology Stack

### Backend
- **Django**: Python web framework
- **Django REST Framework**: API development
- **PostgreSQL/MySQL**: Database (configurable)
- **Authentication**: Django's built-in auth system

### Frontend
- **HTML5/CSS3**: Responsive design with modern CSS
- **JavaScript**: Interactive features and API calls
- **Font Awesome**: Icon library
- **Marked.js**: Markdown rendering for AI responses

## 📁 Project Structure

```
doctor-ai/
├── doctor_ai/
| ├── __init__.py
| ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── chat/
| ├── __init__.py
| ├── admin.py
| ├── ai_service.py
| ├── apps.py
│ ├── models.py
| ├── tests.py
│ ├── views.py
│ ├── urls.py
│ ├── 
│ └──
├── static/
│ ├── images/
| |   └──  logo.png   
│ └── css/
├── templates/
│   ├── base.html
|   └── chat/
│       ├── chat.html
│       ├── dashboard.html
│       ├── login.html
│       ├── register.html
│   └── components/
│       ├── analysis_sections.html
│       ├── sidebar.html
│       ├── auth_header.html
│       ├── chat_container.html
│       └── mobile_menu.html
└── manage.py
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.0+
- Database (PostgreSQL recommended)
- Virtual environment tool (venv or conda)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd doctor-ai
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements
   ```

4. **Configure Database**
   - Update `settings.py` with your database credentials
   - Choose PostgreSQL, MySQL, or SQLite (for development)

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access Application**
   - Open browser: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/doctor_ai
```

### Settings to Configure
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (set to False in production)
- `ALLOWED_HOSTS`: Domain names for production
- `DATABASES`: Database configuration
- `STATIC_ROOT`: Static files directory for production
- `MEDIA_ROOT`: Media files directory

## 🎨 UI Components

### 1. **Sidebar**
- Collapsible chat history
- Tooltips for collapsed state
- Mobile-responsive with hamburger menu
- Login prompt for guests

### 2. **Chat Interface**
- AI and user message bubbles
- Markdown support for AI responses
- Typing indicator
- Responsive avatar placement
- Smooth scrolling

### 3. **Dashboard**
- User statistics and session overview
- Quick action buttons
- Recent health analyses
- Mobile-optimized layout

### 4. **Authentication System**
- Login/Registration forms
- Session management
- Guest mode
- User profile display



## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 1024px (Full sidebar, two-column layout)
- **Tablet**: 768px - 1024px (Responsive sidebar, single column)
- **Mobile**: < 768px (Hamburger menu, stacked layout)

### Mobile Features
- Touch-friendly buttons and inputs
- Swipe gestures for sidebar
- Optimized chat bubbles
- Adaptive font sizes

## 🔐 Security Features

- Django's built-in CSRF protection
- Secure password handling
- Session-based authentication
- SQL injection protection
- XSS prevention through template escaping



## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Set up a production database
4. Collect static files: `python manage.py collectstatic`
5. Set up web server (Nginx + Gunicorn recommended)
6. Configure SSL certificates
7. Set up logging

### Deployment Options
- **Heroku**: Easy Django deployment
- **AWS Elastic Beanstalk**: Scalable deployment
- **DigitalOcean**: Simple VPS setup
- **PythonAnywhere**: Beginner-friendly hosting

## 📊 Database Models

### Key Models
1. **User**: Extended Django user model
2. **ChatMessage**: Individual chat messages
3. **AnalysisSession**: Stores conversation metadata

## 🔄 Workflow

1. **User Registration/Login**
2. **Select Analysis Category**
3. **Interactive Chat with AI**
4. **Save Conversation**
5. **Review History in Dashboard**
6. **Continue Previous Sessions**

## ⚠️ Important Notes

### Medical Disclaimer
This application is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.

### Limitations
- AI responses are based on patterns and general knowledge
- No real-time medical data integration
- No emergency response capabilities
- Not HIPAA compliant (for development only)

## 🆘 Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` in settings

2. **Database connection errors**
   - Verify database credentials
   - Ensure database server is running

3. **API endpoints returning 404**
   - Check URL patterns in `urls.py`
   - Verify API views are properly registered

4. **Mobile sidebar not working**
   - Check JavaScript console for errors
   - Verify viewport meta tag is present

### Debug Mode
When `DEBUG = True`, detailed error pages will show:
- Django version
- Settings information
- Request details
- Traceback information

## 📈 Future Enhancements

### Planned Features
1. **Health Data Integration**
   - Wearable device data sync
   - Medical record import
   - Lab result analysis

2. **Advanced AI Features**
   - Multilingual support
   - Voice input/output
   - Image analysis (food logging, exercise form)

3. **User Experience**
   - Dark mode
   - Custom themes
   - Export conversations
   - Health reports and insights

4. **Collaboration**
   - Share analyses with healthcare providers
   - Family health tracking
   - Group wellness challenges

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request
5. Ensure code follows PEP 8 standards

## 📄 License

This project is for educational purposes. For commercial use, please ensure compliance with medical software regulations in your jurisdiction.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Font Awesome for icons
- Marked.js for markdown rendering
- All contributors and testers

---

## 📞 Support

For issues, feature requests, or questions:
- Create a GitHub issue
- Check the documentation
- Review existing issues for solutions

---

**Remember**: This tool is designed to supplement, not replace, professional medical care. Always prioritize consultation with qualified healthcare providers for medical decisions.