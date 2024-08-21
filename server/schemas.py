from __future__ import annotations

from typing import Any
from typing_extensions import Annotated
from uuid import UUID
from datetime import time, datetime

from pydantic import BaseModel, FutureDatetime, Field
from pydantic.functional_validators import AfterValidator


def validate_pagination_limit(value: int):
    assert 0 <= value <= 50
    return value


def validate_pagination_offset(value: int):
    assert 0 <= value
    return value


PaginationLimit = Annotated[int, AfterValidator(validate_pagination_limit)]
PaginationOffset = Annotated[int, AfterValidator(validate_pagination_offset)]


class MeetSchema(BaseModel):
    datetime: FutureDatetime
    place_address: str
    place_longtitude: float
    place_latitude: float


class PostMeetSchema(MeetSchema):
    operations_ids: list[int]


class PersonSchema(BaseModel):
    name: str
    surname: str
    position: str


class GetMeetSchema(PostMeetSchema):
    id: UUID
    representative_id: int | None
    approximate_end_datetime: datetime
    client_side_people: list[PersonSchema]


class PostCrunchMeetSchema(BaseModel):
    datetime: FutureDatetime
    place_address: str
    place_longtitude: float
    place_latitude: float
    operations_names: list[str]


class PostRepresentativeSchema(BaseModel):
    name: str
    surname: str
    photo_inner_url: str
    position: str


class RepresentativeSchema(PostRepresentativeSchema):
    id: int


class PostOperationSchema(BaseModel):
    name: str
    product: str
    documents: list[str]
    duration: time  # SUCKS


class OperationSchema(PostOperationSchema):
    id: int


class PatchMeetSchema(BaseModel):
    datetime: FutureDatetime | None = None
    place_address: str | None = None
    place_longtitude: float | None = None
    place_latitude: float | None = None
    operations_ids: list[int] | None = None


class ClientSchema(BaseModel):
    id: Any | None
    name: str
    logo_url: str | None


class OperationsRequestSchema(BaseModel):
    ids: list[int]


class ProtectedIntIDPointer(BaseModel):
    key: str
    id: int
