from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()
    
    e1 = Exercise(name='Push-Up', category='Strength', equipment_needed=False)
    e2 = Exercise(name='Running', category='Cardio', equipment_needed=True)
    e3 = Exercise(name='Yoga', category='Flexibility', equipment_needed=False)
    e4 = Exercise(name='Plank', category='Balance', equipment_needed=False)
    e5 = Exercise(name='Jumping Jacks', category='Cardio', equipment_needed=False)
    e6 = Exercise(name='Dumbell Curl', category='Strength', equipment_needed=True)
    
    db.session.add_all([e1, e2, e3, e4, e5, e6])
    db.session.commit()