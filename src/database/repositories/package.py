from decimal import Decimal
from typing import List, Tuple, Optional, Sequence

from sqlalchemy import select, update, bindparam, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from delivery_service.src.schemas.package import Package as PackageSchema, \
    CreateTypePackage
from delivery_service.src.database.models.package import Package, TypePackage


class PackageRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, package: PackageSchema) -> Package:
        stmt = Package(
            name=package.name,
            weight=package.weight,
            price_usd=package.price_usd,
            delivery_price=package.delivery_price,
            session_id=package.session_id,
            type_id=package.type.id
        )
        async with self.db_session as session:
            session.add(stmt)
            await session.commit()
        return stmt

    async def get_packages(self, session_id: str):
        query = select(Package).where(Package.session_id == session_id)
        async with self.db_session as session:
            result = await session.execute(query)
            packages = result.scalars().all()
            return packages

    async def get_by_id(self,
                        session_id: str,
                        package_id: int):
        query = select(Package).where(Package.id == package_id,
                                      Package.session_id == session_id)
        async with self.db_session as session:
            ex = await session.execute(query)
            result = ex.scalars().all()
        return result

    async def get_all(self, db_session):
        query = select(Package)
        async with db_session as session:
            ex = await session.execute(query)
            result = ex.scalars().all()
        return result

    async def update_calc_bulk(self, db_session, updates: List[Tuple[int, Decimal]]):
        # stmt = update(Package).where(
        #     Package.id == bindparam('id')
        # ).values(delivery_price=bindparam('delivery_price')
        #          ).execution_options(synchronize_session=False)
        # async with db_session as session:
        #     await session.execute(stmt, [
        #         {'id': _id, 'delivery_price': delivery_price}
        #         for _id, delivery_price in updates
        #     ])
        #     await session.commit()
        params = [
            {"pkg_id": id_, "price_val": float(price)}
            for id_, price in updates
        ]

        stmt = (
            update(Package)
            .where(Package.id == bindparam("pkg_id"))
            .values(delivery_price=bindparam("price_val"))
            .execution_options(synchronize_session=False)
        )

        result = await db_session.execute(stmt, params)
        await db_session.commit()


class TypePackageRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> [TypePackage]:
        async with self.db_session as session:
            result = await session.execute(select(TypePackage))
            return result.scalars().all()

    async def add(self, type_package: CreateTypePackage) -> TypePackage:
        stmt = TypePackage(
            name=type_package.name
        )
        async with self.db_session as session:
            session.add(stmt)
            await session.commit()
        return stmt

