from uuid import UUID

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from server.entities import Meet, Representative, Operation
from server.db.models import (
    MeetModel,
    RepresentativeModel,
    OperationsModel,
)
from server.exceptions import EntityNotFoundInDB

ConnectionProvider = sessionmaker[AsyncSession]  # type: ignore


class Repo:
    __connection_provider: ConnectionProvider

    def __init__(self, connection_provider: ConnectionProvider) -> None:
        self.__connection_provider = connection_provider

    async def get_meet_by_id(self, id: UUID) -> Meet:
        async with self.__connection_provider() as session:
            q = select(MeetModel).where(MeetModel.id == id)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_operation_by_name(self, name: str) -> Meet:
        async with self.__connection_provider() as session:
            q = select(OperationsModel).where(OperationsModel.name == name)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def insert_meet(self, meet: Meet) -> Meet:
        async with self.__connection_provider() as session:
            model = MeetModel(
                id=meet.id,
                client_id=meet.client_id,
                datetime=meet.datetime,
                place_address=meet.place_address,
                place_longtitude=meet.place_longtitude,
                place_latitude=meet.place_latitude,
                operations_ids=meet.operations_ids,
            )

            session.add(model)

            await session.commit()
            return meet

    async def update_meet(self, meet: Meet) -> Meet:
        async with self.__connection_provider() as session:
            model_in_db = await session.get(MeetModel, meet.id)

            if not model_in_db:
                raise EntityNotFoundInDB(f"No such user with id {meet.id}")
            model = MeetModel(
                id=meet.id,
                client_id=meet.client_id,
                datetime=meet.datetime,
                place_address=meet.place_address,
                place_longtitude=meet.place_longtitude,
                place_latitude=meet.place_latitude,
                operations_ids=meet.operations_ids,
            )

            await session.merge(model)

            await session.commit()

            return await self.get_meet_by_id(model.id)

    async def get_all_client_meets(
        self, client_id: int | None = None, limit: int = 10, offset: int = 0
    ):
        async with self.__connection_provider() as session:
            q = (
                select(MeetModel)
                .where(MeetModel.client_id == client_id)
                .order_by(MeetModel.datetime)
                .offset(offset)
                .limit(limit)
            )

            res = (await session.execute(q)).scalars()

            return [await model.as_entity(self).async_post_init() for model in res]

    async def get_representative_by_id(self, id: int):
        async with self.__connection_provider() as session:
            q = select(RepresentativeModel).where(RepresentativeModel.id == id)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_operation_by_id(self, id: int) -> Operation:
        async with self.__connection_provider() as session:
            q = select(OperationsModel).where(OperationsModel.id == id)

            res = (await session.execute(q)).scalar()

            return res and res.as_entity(self)

    async def get_all_operations(self) -> list[Operation]:
        async with self.__connection_provider() as session:
            q = select(OperationsModel)

            res = (await session.execute(q)).scalars()

            return [model.as_entity(self) for model in res]

    async def insert_operation(self, operation: Operation) -> Operation:
        async with self.__connection_provider() as session:
            model = OperationsModel(
                name=operation.name,
                product=operation.product,
                documents=operation.documents,
                duration=operation.duration,
            )

            session.add(model)

            await session.commit()
            return await self.get_operation_by_id(model.id)

    async def insert_representative(
        self, representative: Representative
    ) -> Representative:
        async with self.__connection_provider() as session:
            model = RepresentativeModel(
                name=representative.name,
                surname=representative.surname,
                photo_inner_url=representative.photo_inner_url,
            )

            session.add(model)

            await session.commit()
            return await self.get_representative_by_id(model.id)

    async def delete_meet(self, meet_id: UUID):
        async with self.__connection_provider() as session:
            model = await session.get(MeetModel, meet_id)

            if not model:
                raise EntityNotFoundInDB(f"No such meet with id {meet_id}")

            await session.delete(model)
            await session.commit()
            return model.as_entity(self)

    async def get_operations_by_ids(self, ids):
        return [await self.get_operation_by_id(id) for id in ids]

    async def get_all_representative_meets(
        self, representative_id: int | None = None, limit: int = 10, offset: int = 0
    ):
        async with self.__connection_provider() as session:
            q = (
                select(MeetModel)
                .where(MeetModel.representative_id == representative_id)
                .order_by(MeetModel.datetime)
                .offset(offset)
                .limit(limit)
            )

            res = (await session.execute(q)).scalars()

            return [await model.as_entity(self).async_post_init() for model in res]

    async def delete_operation(self, operation_id: int):
        async with self.__connection_provider() as session:
            model = await session.get(OperationsModel, operation_id)

            if not model:
                raise EntityNotFoundInDB(f"No such operation with id {operation_id}")

            await session.delete(model)
            await session.commit()
            return model.as_entity(self)

    async def delete_representative(self, representative_id: int):
        async with self.__connection_provider() as session:
            model = await session.get(RepresentativeModel, representative_id)

            if not model:
                raise EntityNotFoundInDB(
                    f"No such representative with id {representative_id}"
                )

            await session.delete(model)
            await session.commit()
            return model.as_entity(self)

    async def delete_meets(self):
        async with self.__connection_provider() as session:
            q = delete(MeetModel)

            await session.execute(q)

            await session.commit()

    async def delete_operations(self):
        async with self.__connection_provider() as session:
            q = delete(OperationsModel)

            await session.execute(q)

            await session.commit()

    async def delete_representatives(self):
        async with self.__connection_provider() as session:
            q = delete(RepresentativeModel)

            await session.execute(q)

            await session.commit()
