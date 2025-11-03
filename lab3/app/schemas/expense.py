
from marshmallow import Schema, fields, validate

class ExpenseCreateSchema(Schema):
    amount = fields.Decimal(as_string=True, required=True, validate=validate.Range(min=0))
    description = fields.Str(load_default=None, validate=validate.Length(max=255))
    category_id = fields.Int(load_default=None)

class ExpensePatchSchema(Schema):
    amount = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    description = fields.Str(validate=validate.Length(max=255))
    category_id = fields.Int()

class ExpenseOutSchema(Schema):
    id = fields.Int(required=True)
    amount = fields.Decimal(as_string=True, required=True)
    description = fields.Str(allow_none=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(allow_none=True)
