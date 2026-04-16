from flask_sqlachemy import SQLAlchemy
from sqlachemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    
    workout_excercises = db.relationship
    workouts = 