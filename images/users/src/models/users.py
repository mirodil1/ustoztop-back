from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import backref, relationship

from src.models.core import TimeStampedModel
from src.db import db

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
    is_confirmed_by_admin = db.Column(db.Boolean, default=False)
    is_promoted = db.Column(db.Boolean, default=False)
    promotion_started = db.Column(db.Date, nullable=True)
    promotion_expired = db.Column(db.Date, nullable=True)
    

    tutor = relationship("Tutor", uselist=False, back_populates="user")
    learning_center = relationship("LearningCenter", uselist=False, back_populates="user")

    logins = relationship(
        "LoginRecord",
        lazy="dynamic",
        cascade="all, delete-orphan",
        backref=backref("user"),
    )


class Role(TimeStampedModel):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255), nullable=True)
    permissions = db.Column(ARRAY(db.String, dimensions=1), default=[], nullable=True)

    # @classmethod
    # def get(cls, name):
    #     role = session.query(cls).filter_by(name=name).one_or_none()
    #     if not role:
    #         raise NotFound(f"Role with name {name} is not found")


class RolesUsers(TimeStampedModel):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.ForeignKey("users.id"))
    role_id = db.Column("role_id", db.Integer, db.ForeignKey("roles.id"))


class LoginRecord(TimeStampedModel):
    __tablename__ = "login_entries"

    id = db.Column(db.BigInteger, primary_key=True, unique=True)
    user_id = db.Column("user_id", db.ForeignKey("users.id"))
    user_agent = db.Column(db.String)
    platform = db.Column(db.String(100))
    browser = db.Column(db.String(255))
    ip = db.Column(db.String(100))

    def __init__(self, user_id, platform, browser, user_agent, ip):
        self.user_id = user_id
        self.platform = platform
        self.browser = browser
        self.user_agent = user_agent
        self.ip = ip

    # def to_api_model(self) -> UserLoginRecord:
    #     return UserLoginRecord(
    #         user_agent=self.user_agent,
    #         platform=self.platform,
    #         browser=self.browser,
    #         timestamp=self.timestamp,
    #         ip=self.ip,
    #     )
