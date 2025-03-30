from decimal import Decimal
from typing import List, Tuple

from sqlalchemy import select, update, bindparam
from sqlalchemy.orm import Session

from delivery_service.src.schemas.package import Package as PackageSchema
from delivery_service.src.database.models.package import Package, TypePackage


class PackageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, package: PackageSchema) -> Package:
        async with self.db_session as session:
            pass

    async def get_packages(self,
                      session_id: str) -> List[Package]:
        async with self.db_session as session:
            pass

    async def get_by_id(self,
                        session_id: str,
                        package_id: int) -> Package:
        async with self.db_session as session:
            pass

    async def get_all(self):
        query = select(Package)
        async with self.db_session as session:
            ex = await session.execute(query)
            result = ex.scalars.all()
            return result

    async def update_calc_bulk(self, updates: List[Tuple[int, Decimal]]):
        stmt = update(Package).where(
            Package.id == bindparam('id')
        ).values(delivery_price=bindparam('delivery_price'))
        async with self.db_session as session:
            await session.execute(stmt, [
                {'id': _id, 'delivery_price': delivery_price}
                for _id, delivery_price in updates
            ])
            await session.commit()


class TypePackageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all(self) -> List[TypePackage]:
        async with self.db_session as session:
            pass
