import datetime
import uuid

from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import UniqueConstraint

from src.db import db
from src.models.core import TimeStampedModel


class LoginHistoryRecord(db.Model):
    __tablename__ = "login_history"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False,
    )
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    device_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("devices.id"), nullable=False,
    )
    login_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    device_type = db.Column(db.String, primary_key=True, default="web", nullable=False)

    UniqueConstraint("id", "device_type", name="id_device_type_pk")

    def __repr__(self):
        return f"<LoginHistoryRecord user={self.user_id} \
            device={self.device_id} date={self.login_date}>"


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    user_agent = db.Column(db.Text)
    history_records = relationship("LoginHistoryRecord", backref="device")

    def __repr__(self):
        return f"<Device id={self.id}, user_id={self.user_id}>"

user_role_asscoations = db.Table(
    "user_role_association",
    db.Column(
        "user_id",
        db.BigInteger,
        db.ForeignKey("users.id"),
        primary_key=True,
    ),
    db.Column(
        "role_id",
        UUID(as_uuid=True),
        db.ForeignKey("roles.id"),
        primary_key=True),
    )


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    role_name = db.Column(db.String, unique=True, nullable=False)
    users = relationship(
        "User",
        secondary="user_role_association",
        back_populates="roles")


class User(TimeStampedModel):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    phone_number = db.Column(db.String(length=14), unique=True, nullable=False)
    email = db.Column(db.String(length=255), unique=True, nullable=True)
    password = db.Column("password", db.String(length=255), nullable=False)
    avatar = db.Column(db.String(length=255), nullable=True)
    web_link = db.Column(db.String(length=255), nullable=True)
    insta_link = db.Column(db.String(length=255), nullable=True)
    facebook_link = db.Column(db.String(length=255), nullable=True)
    telegram_link = db.Column(db.String(length=255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_verified_by_admin = db.Column(db.Boolean, default=False)
    is_premium = db.Column(db.Boolean, default=False)
    premium_started = db.Column(db.Date, nullable=True)
    premium_expired = db.Column(db.Date, nullable=True)

    devices = relationship("Device", backref=backref("user", uselist=False))
    roles = relationship(
        "Role",
        secondary="user_role_association",
        back_populates="users")

    tutor = relationship("Tutor", uselist=False, back_populates="user")
    learning_center = relationship(
        "LearningCenter",
        uselist=False,
        back_populates="user",
    )
