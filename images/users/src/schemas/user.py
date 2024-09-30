from marshmallow import Schema, fields


class UserSchema(Schema):
    phone_number = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
