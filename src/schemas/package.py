from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class TypePackage(BaseModel):
    id: int
    name: str


class Package(BaseModel):
    name: str = Field('Название посылки')
    weight: str = Field('Вес посылки', gt=0)
    type: TypePackage = Field('Тип посылки')
    price_usd: Decimal = Field('Стоимость посылки в $', gt=0)
    delivery_price: Decimal | str = Field('Стоимость доставки', gt=0)

    @field_validator('price_usd')
    def round_decimal(cls, v):
        return round(v, 2)


class CreatePackage(Package):
    pass


class PackageResponse(BaseModel):
    id: int
    name: str
    session_id: str
