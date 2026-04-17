from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()
    