# eduGate - AI-Powered Assignment Submission System launched 31 July 2025

A Flask-based web application for managing student assignments with AI-powered plagiarism detection.

## 🚀 Features

- **Student Portal**: Submit assignments and view submission history
- **Admin Dashboard**: Create assignments, manage students, and view all submissions
- **AI Detection**: Uses Hugging Face models to detect AI-generated content
- **File Management**: Secure PDF upload and storage system
- **User Authentication**: Separate login systems for students and admins


## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd eduGate
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DATABASE_URL="your-database-url"
   export FLASK_ENV="production"
   ```

5. **Initialize database**
   ```bash
   python -c "from main import db; db.create_all()"
   ```

## 🧪 Testing

### Run all tests
```bash
python -m pytest test_app.py -v
```

### Run specific test categories
```bash
# Unit tests
python -m pytest test_app.py::EduGateTestCase::test_database_models -v

# Integration tests
python -m pytest test_app.py::EduGateTestCase::test_student_login -v

# Security tests
python -m pytest test_app.py::EduGateTestCase::test_file_upload_security -v
```

## 🚀 Deployment

### Development
```bash
export FLASK_ENV=development
python main.py
```

### Production
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Using Waitress (Windows)
```bash
waitress-serve --host=0.0.0.0 --port=8000 main:app
```

## 📁 Project Structure

```
eduGate/
├── main.py              # Main Flask application
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── test_app.py         # Test suite
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── uploads/           # File upload directory
├── outputs/           # AI analysis outputs
└── instance/          # Database files
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Production database URL
- `FLASK_ENV`: Environment (development/production)
- `UPLOAD_FOLDER`: File upload directory
- `MAX_CONTENT_LENGTH`: Maximum file upload size

### Security Settings
- File type validation (PDF only)
- File size limits (16MB)
- Session security
- CSRF protection

## 🐛 Troubleshooting

### Common Issues

1. **Database errors**
   ```bash
   python -c "from main import db; db.create_all()"
   ```

2. **Import errors**
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission errors**
   ```bash
   chmod 755 uploads/ outputs/
   ```

## 📞 Support

For issues and questions email eduGate.se@gmail.com:
- Check the troubleshooting section
- Review error logs
- Test with the provided test suite

## 🔒 Security Notes

- Always use HTTPS in production
- Regularly update dependencies
- Monitor file uploads for malicious content
- Implement rate limiting for production
- Set up proper logging and monitoring