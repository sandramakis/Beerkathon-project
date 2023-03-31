from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from ..models.employees import Employee, Admin
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity, create_access_token, create_refresh_token, unset_jwt_cookies, JWTManager
from datetime import timedelta
from ..utils.decorators import admin_required


auth_ns = Namespace('auth', description='Authentication related operations')

signup_model = auth_ns.model(
    'Signup', {
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password': fields.String(required=True, description="A password")
    }
)

user_model = auth_ns.model(
    'Employee', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A username"),
        'email': fields.String(required=True, description="An email"),
        'password_hash': fields.String(required=True, description="A password"),
        'is_admin': fields.Boolean(description="Those who can create meals")
    }
)

login_model = auth_ns.model(
    'Login', {
        'username': fields.String(required=True, description="A username"),
        'password': fields.String(required=True, description="A password")
    }
)

@auth_ns.route('/admin/signup')
class AdminSignUp(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.doc(description='Sign up a new admin')
    def post(self):
        """
            Sign up a new admin
        """

        data = request.get_json()

        user = Employee.get_by_email(data.get('email'))

        # check if user already exists
        if user:
            return {'message': 'User already exists'}, HTTPStatus.BAD_REQUEST

        admin = Admin(
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password')),
            role = 'admin',
            is_admin = True
        )

        admin.save()

        return {
            'message': 'Admin created successfully'
        }, HTTPStatus.CREATED


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.doc(description='Login a user')
    def post(self):
        """
            Login a user
        """

        data = request.get_json()

        username = data.get('username')

        password = data.get('password')

        # check if username and password are provided
        if not username and not password:
            return {
                'message': 'Username and password are required'
            }, HTTPStatus.BAD_REQUEST

        user = Employee.get_by_username(username)

        # check if user exists
        if not user:
            return {
                'message': 'User not found'
            }, HTTPStatus.NOT_FOUND

        # check if password is correct
        if not check_password_hash(user.password_hash, password):
            return {
                'message': 'Wrong password'
            }, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=30))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, HTTPStatus.OK
    

@auth_ns.route('/refresh')
class Refresh(Resource):
    @auth_ns.doc(description='Refresh access token')
    @jwt_required(refresh=True)
    def post(self):
        """
            Refresh access token
        """

        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user, expires_delta=timedelta(hours=1))

        return {
            'access_token': access_token
        }, HTTPStatus.OK
    

@auth_ns.route('/logout')
class Logout(Resource):
    @auth_ns.doc(description='Logout a user')
    @jwt_required()
    def post(self):
        """
            Logout a user
        """

        jti = get_jwt()['jti']

        return {
            'message': 'Successfully logged out'
        }, HTTPStatus.OK
    

@auth_ns.route('/employee')
class AdminAddEmployee(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.doc(description='Admin only can add an employee')
    @admin_required()
    def post(self):
        """
            Add an employee
        """

        data = request.get_json()

        user = Employee.get_by_email(data.get('email'))

        # check if user already exists
        if user:
            return {'message': 'User already exists'}, HTTPStatus.BAD_REQUEST

        new_employee = Employee(
            username = data.get('username'),
            email = data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            
        )

        new_employee.save()

        return {
            'message': 'User created successfully'
        }, HTTPStatus.CREATED
    
    # get all employees
    @auth_ns.marshal_list_with(user_model)
    @auth_ns.doc(description='Get all employees')
    @admin_required()
    def get(self):
        """
            Get all employees
        """

        employees = Employee.get_all()

        return employees, HTTPStatus.OK
    
@auth_ns.route('/employee/<int:id>')
class AdminDeleteEmployee(Resource):
    @auth_ns.doc(description='Admin can delete an employee')
    @admin_required()
    def delete(self, id):
        """
            Delete an employee
        """

        employee = Employee.get_by_id(id)

        if not employee:
            return {'message': 'Employee not found'}, HTTPStatus.NOT_FOUND

        employee.delete()

        return {'message': 'Employee deleted successfully'}, HTTPStatus.OK
    

