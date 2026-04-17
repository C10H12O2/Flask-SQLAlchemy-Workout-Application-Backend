from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """Return a list of all workouts."""
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    """Return a single workout with its associated exercises."""
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout."""
    data = request.get_json()
    try:
        validated_data = workout_schema.load(data)
        workout = Workout(**validated_data)
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout and its associated workout exercises."""
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted successfully'}), 200

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """Return a list of all exercises."""
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    """Return a single exercise with its associated workouts."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create a new exercise."""
    data = request.get_json()
    try:
        validated_data = exercise_schema.load(data)
        exercise = Exercise(**validated_data)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise and its associated workout exercises."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted successfully'}), 200

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an exercise to a workout with reps, sets, or duration."""
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    data = request.get_json()
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id

    try:
        validated_data = workout_exercise_schema.load(data)
        workout_exercise = WorkoutExercise(**validated_data)
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)