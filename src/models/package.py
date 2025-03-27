from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from delivery_service.src.db import Base


class TypePackage(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    package = relationship("Package", back_populates="type")


class Package(Base):
    __tablename__ = "package"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    price_usd = Column(Float, nullable=False)
    delivery_price = Column(Float, nullable=True)
    session_id = Column(String, nullable=False)

    type_id = Column(Integer, ForeignKey('type.id'))
