from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class TypePackage(BaseModel):
    id: int
    name: str


class PackageResponse(BaseModel):
    id: int
    name: str


class Package(BaseModel):
    name: str
    weight: str
    type: TypePackage
    price_usd: Decimal
    delivery_price: Decimal | str
    session_id: str | None

    @field_validator('price_usd')
    def round_decimal(cls, v):
        return round(v, 2)

    def to_response(self, package_id: int) -> PackageResponse:
        return PackageResponse(
            id=package_id,
            name=self.name,
        )


class CreatePackage(Package):
    pass
