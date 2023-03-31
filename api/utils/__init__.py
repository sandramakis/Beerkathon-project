from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from http import HTTPStatus
from ..models.employees import Employee

db = SQLAlchemy()


def get_user_type(id: int):
    '''
    Get the type of user type
    '''

    user = Employee.query.filter_by(id=id).first()

    if user:
        return user.user_type
    
    return None


def admin_required():
    '''
    Custom decorator to check if the user is an admin
    '''
    def wrapper(fn):
        @wraps(fn)

        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if not get_user_type(claims['sub']) == 'admin':
                return {'message': 'You are not authorized to view this page.'}, HTTPStatus.UNAUTHORIZED      
            
            return fn(*args, **kwargs)
        
        return decorated
    
    return wrapper