from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class List(Base):
    """ The SQLAlchemy declarative model class for a List object. """
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
