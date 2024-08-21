from fastapi import APIRouter, HTTPException

from server import repo
from server.schemas import RepresentativeSchema


representatives_router = APIRouter()


@representatives_router.get(
    "/representatives/{id}", response_model=RepresentativeSchema
)
async def get_representative(id: int):
    representative = await repo.get_representative_by_id(id)
    if not representative:
        raise HTTPException(
            status_code=404, detail=f"Representative with id {id} not found"
        )
    return representative
