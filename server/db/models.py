from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    Integer,
    String,
    Uuid,
    Float,
    ForeignKey,
    TIMESTAMP,
    DateTime,
    ARRAY,
    TIME,
)

from server.db.settings import Base as BaseModel  # bad code but ok
from server.entities import Meet, Representative, Operation


if TYPE_CHECKING:
    from server.db.repo import Repo


class RepresentativeModel(BaseModel):
    __tablename__ = "representatives"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    surname = Column(String)
    photo_inner_url = Column(String)
    position = Column(String)

    def as_entity(self, repo: Repo):
        return Representative(
            id=self.id,
            name=self.name,
            surname=self.surname,
            photo_inner_url=self.photo_inner_url,
            position=self.position,
            repo=repo,
        )


class MeetModel(BaseModel):
    __tablename__ = "meets"

    id = Column(Uuid, primary_key=True, unique=True)
    client_id = Column(Integer, nullable=True, default=None)  # None = MVPs
    datetime = Column(DateTime)
    place_address = Column(String)
    place_longtitude = Column(Float)
    place_latitude = Column(Float)
    operations_ids = Column(ARRAY(Integer))
    representative_id = Column(ForeignKey(RepresentativeModel.id))

    def as_entity(self, repo: Repo):
        return Meet(
            id=self.id,
            client_id=self.client_id,
            datetime=self.datetime,
            place_address=self.place_address,
            place_latitude=self.place_latitude,
            place_longtitude=self.place_longtitude,
            operations_ids=self.operations_ids,
            representative_id=self.representative_id,
            repo=repo,
        )


class OperationsModel(BaseModel):
    __tablename__ = "operations"

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    name = Column(String)
    product = Column(String)
    documents = Column(ARRAY(String))
    duration = Column(TIME)

    def as_entity(self, repo: Repo):
        return Operation(
            id=self.id,
            name=self.name,
            product=self.product,
            documents=self.documents,
            duration=self.duration,
            repo=repo,
        )
