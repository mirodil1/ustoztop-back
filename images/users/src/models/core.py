from sqlalchemy.sql import func

from src.db import db


class TimeStampedModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
