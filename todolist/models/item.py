from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from .meta import Base


class Item(Base):
    """ The SQLAlchemy declarative model class for a Item object. """
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    item_text = Column(Text, nullable=False, unique=False)
    completed = Column(Boolean, nullable=True, default=False)

    list_id = Column(Integer, ForeignKey('lists.id'), nullable=False)
    list = relationship('List', backref='items')
