from ..utils import db


class Employee(db.Model):
    __tablename__="employees"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    meal_used = db.Column(db.Integer, default=0)
    meal = db.relationship("Meal", backref="employee", lazy=True)

    user_type = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': user_type
    }
    

    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    

class Admin(Employee):
    __tablename__ = "admins"
    id = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    role = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __repr__(self):
        return f"<Admin {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()