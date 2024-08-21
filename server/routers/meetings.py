from typing import Annotated
from uuid import UUID
from datetime import datetime
import requests

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from server import repo
from server.schemas import (
    PostMeetSchema,
    GetMeetSchema,
    PaginationLimit,
    PaginationOffset,
    PatchMeetSchema,
    PostCrunchMeetSchema,
)
from server.entities import Meet
from server.exceptions import EntityNotFoundInDB
from server.config import WORKER_URL


meetings_router = APIRouter()


@meetings_router.post("/meet", response_model=GetMeetSchema)
async def new_meet(meet_request: PostMeetSchema):
    # if meet_request.datetime < datetime.now(meet_request.datetime.tzinfo):
    #   raise HTTPException(status_code=400, detail="Can't plan meetings in the past!")
    if not all(await repo.get_operations_by_ids(meet_request.operations_ids)):
        raise HTTPException(status_code=400, detail="Such operations does not exist")
    meet = Meet(
        datetime=meet_request.datetime,
        place_address=meet_request.place_address,
        place_longtitude=meet_request.place_longtitude,
        place_latitude=meet_request.place_latitude,
        operations_ids=meet_request.operations_ids,
        repo=repo,
    )
    await repo.insert_meet(meet)
    requests.get(WORKER_URL + "appoint", json={"meet_id": str(meet.id)})

    meet = await repo.get_meet_by_id(meet.id)
    await meet.async_post_init()
    return meet


@meetings_router.post("/meet_alt", response_model=GetMeetSchema)
async def new_meet_alt(meet_request: PostCrunchMeetSchema):
    meet = Meet(
        datetime=meet_request.datetime,
        place_address=meet_request.place_address,
        place_longtitude=meet_request.place_longtitude,
        place_latitude=meet_request.place_latitude,
        operations_ids=[
            (await repo.get_operation_by_name(name)).id
            for name in meet_request.operations_names
        ],
        repo=repo,
    )
    await repo.insert_meet(meet)
    requests.get(WORKER_URL + "appoint", json={"meet_id": str(meet.id)})

    meet = await repo.get_meet_by_id(meet.id)
    await meet.async_post_init()
    return meet


@meetings_router.get("/meet/{id}", response_model=GetMeetSchema)
async def get_meet(id: UUID):
    meet: Meet = await repo.get_meet_by_id(id)

    if not meet:
        raise HTTPException(status_code=404, detail=f"Meet with id {id} not found")

    await meet.async_post_init()
    return meet


@meetings_router.get("/meets", response_model=list[GetMeetSchema])
async def get_meets(
    limit: Annotated[PaginationLimit, Query()] = 100,
    offset: Annotated[PaginationOffset, Query()] = 0,
):
    meets = await repo.get_all_client_meets(limit=limit, offset=offset)

    return meets


@meetings_router.get("/representatives/{id}/meets", response_model=list[GetMeetSchema])
async def get_repr_meets(
    id: int,
    limit: Annotated[PaginationLimit, Query()] = 100,
    offset: Annotated[PaginationOffset, Query()] = 0,
):
    meets = await repo.get_all_representative_meets(
        representative_id=id, limit=limit, offset=offset
    )

    return meets


@meetings_router.delete("/meets/{id}")
async def delete_meet(id: UUID):
    try:
        await repo.delete_meet(id)
    except EntityNotFoundInDB:
        raise HTTPException(status_code=404, detail=f"Meet with id {id} not found")
    return JSONResponse({"status": "ok"})


@meetings_router.patch("/meet/{id}", response_model=GetMeetSchema)
async def patch_meet(id: UUID, patch_data: PatchMeetSchema):
    meet: Meet = await repo.get_meet_by_id(id)
    if meet is None:
        raise HTTPException(status_code=404, detail=f"Meet with id {id} not found")
    if patch_data.datetime is not None:
        # if patch_data.datetime < datetime.now(patch_data.datetime.tzinfo):
        #   raise HTTPException(
        #       status_code=400, detail="Can't plan meetings in the past!"
        #   )
        meet.datetime = patch_data.datetime
    if patch_data.operations_ids is not None:
        meet.operations_ids = patch_data.operations_ids
    if patch_data.place_address is not None:
        if None in (
            patch_data.place_address,
            patch_data.place_latitude,
            patch_data.place_longtitude,
        ):
            raise HTTPException(
                status_code=400,
                detail="If the place is being changed, then longtitude, latitude and address must be set together",
            )
        meet.place_longtitude = patch_data.place_longtitude
        meet.place_latitude = patch_data.place_latitude
        meet.place_address = patch_data.place_address

    await repo.update_meet(meet)

    requests.patch(WORKER_URL + "appoint", json={"meet_id": str(meet.id)})

    meet = await repo.get_meet_by_id(meet.id)
    await meet.async_post_init()
    return meet
