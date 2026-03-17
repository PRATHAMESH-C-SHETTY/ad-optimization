import json
import os
import pandas as pd
from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

from routes.dataset_routes import get_active_df
from analytics.eda import (
    summary_stats,
    top_campaigns,
    platform_performance,
    age_group_performance,
    device_performance,
    location_performance,
    ctr_trend,
    conversion_trend
)
from models.optimization_engine import generate_recommendations
from models.ai_optimizer import generate_ai_optimizer_report

analytics_bp = Blueprint('analytics', __name__)


def _load(app, user_id):
    """Load dataset only for the logged-in user"""
    return get_active_df(app, user_id)


@analytics_bp.route('/dashboard')
@login_required
def dashboard():
    df = _load(current_app, current_user.id)
    
    # Get current hour for greeting
    from datetime import datetime
    current_hour = datetime.now().hour
    
    if df is None:
        return render_template(
            'dashboard.html',
            no_data=True,
            has_data=False,
            current_hour=current_hour
        )

    # Only pass necessary data for simplified dashboard
    stats = summary_stats(df)
    top_camp = top_campaigns(df)

    return render_template(
        'dashboard.html',
        stats=stats,
        top_campaigns=top_camp,
        no_data=False,
        has_data=True,
        current_hour=current_hour
    )


@analytics_bp.route('/analytics')
@login_required
def analytics():
    df = _load(current_app, current_user.id)

    if df is None:
        return render_template(
            'analytics.html',
            no_data=True,
            has_data=False
        )

    top_camp = top_campaigns(df, n=10)
    plat_perf = platform_performance(df)
    age_perf = age_group_performance(df)
    dev_perf = device_performance(df)
    loc_perf = location_performance(df)
    ctr_data = ctr_trend(df)
    conv_data = conversion_trend(df)

    return render_template(
        'analytics.html',
        top_campaigns=top_camp,
        platform_perf=plat_perf,
        age_perf=age_perf,
        device_perf=dev_perf,
        loc_perf=loc_perf,
        ctr_trend=ctr_data,
        conv_trend=conv_data,
        no_data=False,
        has_data=True
    )


@analytics_bp.route('/optimization')
@login_required
def optimization():
    df = _load(current_app, current_user.id)

    if df is None:
        return render_template(
            'optimization.html',
            no_data=True,
            has_data=False
        )

    # Get basic recommendations
    recs = generate_recommendations(df)
    
    # Get advanced AI optimizer report
    ai_report = generate_ai_optimizer_report(df)

    return render_template(
        'optimization.html',
        recs=recs,
        ai_report=ai_report,
        no_data=False,
        has_data=True
    )


@analytics_bp.route('/reports')
@login_required
def reports():
    df = _load(current_app, current_user.id)

    if df is None:
        return render_template(
            'reports.html',
            no_data=True,
            has_data=False
        )

    stats = summary_stats(df)
    top_camp = top_campaigns(df, n=10)
    recs = generate_recommendations(df)

    return render_template(
        'reports.html',
        stats=stats,
        top_campaigns=top_camp,
        recs=recs,
        no_data=False,
        has_data=True
    )