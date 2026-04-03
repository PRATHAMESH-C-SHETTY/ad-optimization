import os
from pathlib import Path

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ad-optimizer-secret-2024'
    
    # Database - Support both SQLite and external databases
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        db_path = os.path.join(os.path.dirname(__file__), 'database.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File storage
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(__file__), 'datasets')
    REPORT_FOLDER = os.environ.get('REPORT_FOLDER') or os.path.join(os.path.dirname(__file__), 'reports')
    
    # Upload size limit
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Environment
    ENVIRONMENT = os.environ.get('ENVIRONMENT') or 'development'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Ensure directories exist
    Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(REPORT_FOLDER).mkdir(parents=True, exist_ok=True)
