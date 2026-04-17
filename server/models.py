from flask_sqlachemy import SQLAlchemy
from sqlachemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    
    workout_excercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade= 'all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')
    
    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Exercise name cannot be empty.")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        allowed = ['Cardio', 'Strength', 'Flexibility', 'Balance', 'Other']
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return value.lower()
    
    def __repr__(self):
        return f'<Exercise {self.name}>'
    
class WorkoutExercise(db.Model):
    ___tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)