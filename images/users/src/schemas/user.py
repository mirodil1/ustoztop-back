from marshmallow import Schema, fields


class UserSchema(Schema):
    phone_number = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(required=True)
    code = fields.String(required=True)


class UserAuthInfoSchema(Schema):
    phone_number = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    device_id = fields.String(load_only=True)
