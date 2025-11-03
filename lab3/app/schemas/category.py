
from marshmallow import Schema, fields, validate

class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    # is_global is managed by server policy in this lab; clients create user-scoped categories.
    is_global = fields.Boolean(load_default=False)

class CategoryOutSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    is_global = fields.Bool(required=True)
    user_id = fields.Int(allow_none=True)
