from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from src.db import Base


class TypePackage(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    package = relationship('Package')


class Package(Base):
    __tablename__ = 'package'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    weight = Column(String(10), nullable=False)
    price_usd = Column(Float, nullable=False)
    delivery_price = Column(Float, nullable=True)
    session_id = Column(String(50), nullable=False)

    type_id = Column(Integer, ForeignKey('type.id'))
