#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from models.base_model import Base


class DBStorage:
    """This class manages storage of hbnb models in a database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates the DBStorage class"""
        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}",
            pool_pre_ping=True
        )

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects of a given class, or all objects if cls is None"""
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        classes = {"State": State, "City": City, "User": User,
                   "Place": Place, "Review": Review, "Amenity": Amenity}

        objects = {}
        if cls is None:
            for model in classes.values():
                for obj in self.__session.query(model).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        else:
            for obj in self.__session.query(cls).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        return objects

    def new(self, obj):
        """Adds a new object to the database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Loads storage dictionary from database"""
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Closes the session"""
        self.__session.remove()

    # New methods added
    def get(self, cls, id):
        """Retrieve one object by class and ID"""
        if cls is None or id is None:
            return None
        return self.__session.query(cls).filter_by(id=id).first()

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls is None:
            return sum(self.__session.query(model).count() for model in Base.__subclasses__())
        return self.__session.query(cls).count()


