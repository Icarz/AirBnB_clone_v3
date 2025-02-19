#!/usr/bin/python3
"""This module defines a base class for all models"""

import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

# Define Base for SQLAlchemy
Base = declarative_base()


class BaseModel:
    """A base class for all AirBnB models"""

    # Define common database columns
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime, default=datetime.utcnow, nullable=False,
        onupdate=datetime.utcnow
    )

    def __init__(self, *args, **kwargs):
        """Initialize a new instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """Return string representation of BaseModel instance"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )
