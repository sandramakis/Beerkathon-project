from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime
from ..models.meals import Meal
from ..models.employees import Employee
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from ..utils.decorators import admin_required


meal_ns = Namespace('meals', description='Meal related operations')

add_meal_model = meal_ns.model(
    'Meal', {
        'name': fields.String(required=True, description="A meal name"),
        'employee_id': fields.Integer(required=True, description="An employee id"),
        # 'date': fields.Date(required=True, description="A date")
    }
)

meal_model = meal_ns.model(
    'Meal', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description="A meal name"),
        'employee_id': fields.Integer(required=True, description="An employee id"),
        'date': fields.Date(description="A date")
    }
)


@meal_ns.route('/meal')
class AssignMeal(Resource):
    @meal_ns.expect(meal_model)
    @meal_ns.doc(description='Admin creates a meal for an employee')
    @admin_required()
    def post(self):
        """
            Create a new meal
        """
        data = request.get_json()

        # employee = Employee.get_by_id(data.get('employee_id'))

        meal = Meal(
            name = data.get('name'),
            employee_id = data.get('employee_id'),
            date = datetime.date.today()
        )

        meal.save()

        employee_meal = {}
        employee_meal['name'] = meal.name
        employee_meal['date'] = meal.date
        employee_meal['employee_id'] = meal.employee_id

        return {
            'meal': employee_meal
        }, HTTPStatus.CREATED


    @meal_ns.marshal_list_with(meal_model)
    @meal_ns.doc(description='Any authenticated user can get all meals')
    @jwt_required()
    def get(self):
        """
            Get all meals
        """
        meals = Meal.get_all()

        return {
            'meals': meals
        }, HTTPStatus.OK
        
# to check if the employee has already used his meal
@meal_ns.route('/meal/<int:employee_id>')
class CheckMeal(Resource):
    @meal_ns.doc(description='Any authenticated user can get a meal')
    @jwt_required()
    def get(self, employee_id):
        """
            Get a meal
        """
        meal = Meal.get_by_id(employee_id)

        employee = Employee.get_by_id(employee_id)

        if not meal:
            return {'message': 'Meal not found'}, HTTPStatus.NOT_FOUND

        if employee.meal_used >= 1:
            return {'message': 'You have already taken your meal today'}, HTTPStatus.BAD_REQUEST
        
        employee.meal_used += 1

        employee.update()

        return {'meal': meal}, HTTPStatus.OK

