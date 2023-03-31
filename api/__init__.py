from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models.employees import Employee, Admin
from .models.meals import Meal
from .auth.views import auth_ns
from .meals.views import meal_ns



def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT token&gt; to authorize **"
        }
    }

    api = Api(app,
              title="Meal Management System",
              description="A simple meal management system",
              authorizations=authorizations,
              security="Bearer Auth"
            )

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(meal_ns, path='/meals')

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Employee": Employee,
            "Meal": Meal,
            "Admin": Admin
        }
    
    return app