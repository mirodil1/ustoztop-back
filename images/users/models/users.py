from sqlalchemy import (
    Array,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import backref, relationship

from models.core import TimeStampedModel


class User(TimeStampedModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    phone_number = Column(String(length=14), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    password = Column("password", String(length=255), nullable=False)
    avatar = Column(String, nullable=True)
    web_link = Column(nullable=True)
    insta_link = Column(nullable=True)
    facebook_link = Column(nullable=True)
    telegram_link = Column(nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    tutor = relationship("Tutor", uselist=False, back_populates="user")

    logins = relationship(
        "LoginRecord",
        lazy="dynamic",
        cascade="all, delete-orphan",
        backref=backref("user"),
    )


class Role(TimeStampedModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(80), unique=True)
    description = Column(String(255), nullable=True)
    permissions = Column(ARRAY(String, dimensions=1), default=[])

    # @classmethod
    # def get(cls, name):
    #     role = session.query(cls).filter_by(name=name).one_or_none()
    #     if not role:
    #         raise NotFound(f"Role with name {name} is not found")


class RolesUsers(TimeStampedModel):
    __tablename__ = "roles_users"
    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    role_id = Column("role_id", Integer, ForeignKey("roles.id"))


class LoginRecord(TimeStampedModel):
    __tablename__ = "login_entries"
    id = Column(BigInteger, primary_key=True, unique=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    user_agent = Column(String)
    platform = Column(String(100))
    browser = Column(String(255))
    ip = Column(String(100))

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
