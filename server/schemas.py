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
        