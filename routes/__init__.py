from flask import Blueprint
from .auth import auth_bp
from .tasks import tasks_bp
from .google_calendar import google_calendar_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(google_calendar_bp, url_prefix='/google_calendar')