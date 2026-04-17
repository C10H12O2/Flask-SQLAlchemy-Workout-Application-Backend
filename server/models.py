from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan', overlaps='workouts')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', overlaps='workout_exercises')
    
    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Exercise name cannot be empty.")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        allowed = ['cardio', 'strength', 'flexibility', 'balance', 'other']
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return value.lower()
    
    def __repr__(self):
        return f'<Exercise {self.name}>'
    
class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan', overlaps='exercises')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', overlaps='workout_exercises')
    
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Duration must be a positive number.")
        return value
    
    @validates('date')
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Date cannot be empty.")
        return value
    
    def __repr__(self):
        return f'<Workout {self.date}>'
    
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    workout = db.relationship('Workout', back_populates='workout_exercises', overlaps='exercises,workouts')
    exercise = db.relationship('Exercise', back_populates='workout_exercises', overlaps='exercises,workouts')
    
    @validates('sets')
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be a positive integer.")
        return value
    
    @validates('reps')
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be a positive integer.")
        return value
    
    def __repr__(self):
        return f'<WorkoutExercise workout = {self.workout_id} exercise = {self.exercise_id}>'
    