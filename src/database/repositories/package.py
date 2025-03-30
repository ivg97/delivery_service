from typing import List

from sqlalchemy.orm import Session

from delivery_service.src.schemas.package import Package as PackageSchema
from delivery_service.src.database.models.package import Package, TypePackage


class PackageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, package: PackageSchema) -> Package:
        async with self.db_session as session:
            pass

    async def get_all(self,
                      session_id: str) -> List[Package]:
        async with self.db_session as session:
            pass

    async def get_by_id(self,
                        session_id: str,
                        package_id: int) -> Package:
        async with self.db_session as session:
            pass


class TypePackageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all(self) -> List[TypePackage]:
        async with self.db_session as session:
            pass
