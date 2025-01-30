from marshmallow import Schema, fields


class RefreshTokenSchema(Schema):
    device_id = fields.UUID(required=True)
    refresh_token = fields.String(required=True)
    phone_number = fields.String(required=True)


class UserSchema(Schema):
    phone_number = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(required=True)
    code = fields.String(required=True)


class UserAuthInfoSchema(Schema):
    phone_number = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    device_id = fields.String(load_only=True)


class UserLocationSchema(Schema):
    uz = fields.String(required=True)
    ru = fields.String(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


class UserUpdateSchema(Schema):
    username = fields.String(required=False)
    phone_number = fields.String(required=False)
    avatar = fields.String(required=False)
    password = fields.String(required=False)
    web_link = fields.String(required=False)
    facebook_link = fields.String(required=False)
    insta_link = fields.String(required=False)
    telegram_link = fields.String(required=False)
    location = fields.Nested(UserLocationSchema, required=False)
    tags = fields.List(fields.Integer, required=False)
