from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from models.ml_models import train_models, predict_performance
from routes.dataset_routes import get_active_df

prediction_bp = Blueprint('prediction', __name__)

PLATFORMS = ['Facebook', 'Instagram', 'Google', 'Twitter', 'LinkedIn', 'TikTok', 'YouTube']
AGE_GROUPS = ['18-24', '25-34', '35-44', '45-54', '55+']
DEVICES = ['Mobile', 'Desktop', 'Tablet']


def _ensure_model(app, user_id):
    """Train model if not already in memory."""
    if user_id not in app.trained_models:
        df = get_active_df(app, user_id)
        if df is None:
            return None
        trained = train_models(df)
        app.trained_models[user_id] = {
            'basic': trained,
            'df': df,
            'last_trained': datetime.now()
        }
    
    model_data = app.trained_models.get(user_id)
    if model_data is None:
        return None
    
    # Handle both old and new cache formats
    if isinstance(model_data, dict):
        return model_data.get('basic')
    else:
        # Old format - direct model storage
        return model_data


@prediction_bp.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
    trained = _ensure_model(current_app, current_user.id)
    model_metrics = {}
    pred_result = None

    if trained:
        for target, models in trained.get('results', {}).items():
            model_metrics[target] = {
                name: {'r2': info['r2'], 'mae': info['mae']}
                for name, info in models.items()
            }

    if request.method == 'POST':
        platform = request.form.get('platform', 'Facebook')
        age_group = request.form.get('age_group', '25-34')
        device = request.form.get('device', 'Mobile')
        budget = float(request.form.get('budget', 1000))
        impressions = float(request.form.get('impressions', 10000))

        if trained is None:
            flash('Please upload a dataset first to enable predictions.', 'warning')
            return redirect(url_for('dataset.upload'))

        # Get fast prediction using pre-trained Random Forest
        pred_result = predict_performance(
            platform=platform, age_group=age_group, device=device,
            budget=budget, impressions=impressions, trained=trained
        )

    return render_template('prediction.html',
                           platforms=PLATFORMS,
                           age_groups=AGE_GROUPS,
                           devices=DEVICES,
                           model_metrics=model_metrics,
                           pred_result=pred_result)
