from models.activity_log import ActivityLog
from models import db

def get_activities_by_user(user_id):
    return ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.created_at.desc()).all()
