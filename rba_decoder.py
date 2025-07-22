from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from flask import jsonify
from controllers.user_controller import get_user_by_id

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = get_user_by_id(user_id)
            roles = [role.name for role in user.roles]
            if not any(role in allowed_roles for role in roles):
                return jsonify({
                    "success": False,
                    "message": "Access forbidden: insufficient permissions"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
