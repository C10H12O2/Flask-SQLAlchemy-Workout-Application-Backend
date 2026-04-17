from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Name cannot be empty."))
    category = fields.Str(required=True, validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'Balance', 'Other'],
                                                                 error="Category must be one of: Cardio, Strength, Flexibility, Balance, Other."))
    equipment_needed = fields.Bool(required=True)