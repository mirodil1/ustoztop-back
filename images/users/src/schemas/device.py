from marshmallow import Schema, fields


class DeviceIdSchema(Schema):
    device_id = fields.UUID(required=False)
