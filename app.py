"""
Smart Ad Optimization and Campaign Analytics Platform
Main Flask Application Entry Point
"""

import os
import io
import uuid
import json
import pandas as pd
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, session, jsonify, send_file, g)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from werkzeug.utils import secure_filename

from config import Config
from models import db, User, Dataset
from utils.data_cleaner import clean_dataset
from analytics.feature_engineering import engineer_features
from analytics.eda import (summary_stats, top_campaigns, platform_performance,
                            age_group_performance, device_performance,
                            location_performance, ctr_trend, conversion_trend)
from models.ml_models import train_models, predict_performance
from models.optimization_engine import generate_recommendations

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.trained_models = {}

    @app.context_processor
    def inject_has_data():
        if current_user.is_authenticated:
            ds = Dataset.query.filter_by(
                user_id=current_user.id, is_active=True
            ).first()
            return {'has_data': ds is not None}
        return {'has_data': False}

    from routes.auth_routes import auth_bp
    from routes.dataset_routes import dataset_bp
    from routes.analytics_routes import analytics_bp
    from routes.prediction_routes import prediction_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(prediction_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('analytics.dashboard'))
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)