from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Name cannot be empty."))
    category = fields.Str(required=True, validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'Balance', 'Other'],
                                                                 error="Category must be one of: Cardio, Strength, Flexibility, Balance, Other."))
    equipment_needed = fields.Bool(required=True)
    
    workouts = fields.List(fields.Nested(lambda: WorkoutSchema(exclude=('exercises',))), dump_only=True)
    
    
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, error_messages={"required": "Date is required."})        
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Duration must be a positive integer."))
    notes = fields.Str()
        
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=('workouts',))), dump_only=True)
    
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(validate=validate.Range(min=1, error="Sets must be a positive integer."))
    reps = fields.Int(validate=validate.Range(min=1, error="Reps must be a positive integer."))
    duration_seconds = fields.Int(validate=validate.Range(min=1, error="Duration must be a positive number."))
    
    exercise = fields.Nested(lambda: ExerciseSchema(exclude=('workouts',)), dump_only=True)
    workout = fields.Nested(lambda: WorkoutSchema(exclude=('exercises',)), dump_only=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
        