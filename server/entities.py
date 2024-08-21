from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, time, timedelta

if TYPE_CHECKING:
    from server.db.repo import Repo


@dataclass
class Person:
    name: str
    surname: str
    position: str


@dataclass
class Meet:
    datetime: datetime
    place_address: str
    place_longtitude: float
    place_latitude: float
    operations_ids: list[int]
    repo: Repo
    id: UUID = field(default_factory=uuid4)
    client_id: int | None = None
    representative_id: int | None = None
    approximate_end_datetime: datetime = field(init=False)
    client_side_people: list[str] = field(
        default_factory=lambda: [
            Person("Тайлер", "Дёрден", "Директор"),
            Person("Патрик", "Бейтман", "Инвестиционный банкир"),
            Person("Райан", "Гослинг", "ПМ"),
        ]
    )  # FIXME: Change hardcoded MVP values

    async def async_post_init(self):
        operations = await self.repo.get_operations_by_ids(self.operations_ids)
        # longest_operation = max(operations, key=lambda x: x.duration)
        # dur = longest_operation.duration
        # self.approximate_end_datetime = self.datetime + timedelta(
        #    seconds=dur.second,
        #    minutes=dur.minute,
        #    hours=dur.hour,
        #    microseconds=dur.microsecond,
        # )

        end_datetime = self.datetime
        for op in operations:
            end_datetime += timedelta(
                seconds=op.duration.second,
                minutes=op.duration.minute,
                hours=op.duration.hour,
                microseconds=op.duration.microsecond,
            )
        self.approximate_end_datetime = end_datetime
        return self


@dataclass
class Representative:
    name: str
    surname: str
    photo_inner_url: str
    position: str
    repo: Repo
    id: int | None = None


@dataclass
class Operation:
    name: str
    product: str
    documents: list[str]
    repo: Repo
    duration: time
    id: int | None = None
