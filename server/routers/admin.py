from fastapi import APIRouter, HTTPException

from server import repo
from server.schemas import (
    PostOperationSchema,
    PostRepresentativeSchema,
    OperationSchema,
    RepresentativeSchema,
    ProtectedIntIDPointer,
)
from server.entities import Operation, Representative

from server.config import ADMIN_TOOLS_KEY

admin_router = APIRouter()


@admin_router.post("/add_operation", response_model=OperationSchema)
async def new_operation(operation: PostOperationSchema):
    operation_entity = Operation(
        name=operation.name,
        product=operation.product,
        documents=operation.documents,
        duration=operation.duration,
        repo=repo,
    )
    return await repo.insert_operation(operation_entity)


@admin_router.post("/add_representative", response_model=RepresentativeSchema)
async def new_representative(representative: PostRepresentativeSchema):
    representative_entity = Representative(
        name=representative.name,
        surname=representative.surname,
        photo_inner_url=representative.photo_inner_url,
        position=representative.position,
        repo=repo,
    )
    return await repo.insert_representative(representative_entity)


@admin_router.delete("/operation")
async def remove_operation(id: ProtectedIntIDPointer):
    if id.key != ADMIN_TOOLS_KEY:
        raise HTTPException(status_code=403, detail="Invalid key")

    return await repo.delete_operation(id.id)


@admin_router.delete("/representative")
async def remove_representative(id: ProtectedIntIDPointer):
    if id.key != ADMIN_TOOLS_KEY:
        raise HTTPException(status_code=403, detail="Invalid key")

    return await repo.delete_representative(id.id)


@admin_router.delete("/representative/all")
async def remove_representatives(id: ProtectedIntIDPointer):
    if id.key != ADMIN_TOOLS_KEY:
        raise HTTPException(status_code=403, detail="Invalid key")

    return await repo.delete_representatives()


@admin_router.delete("/operation/all")
async def remove_operations(id: ProtectedIntIDPointer):
    if id.key != ADMIN_TOOLS_KEY:
        raise HTTPException(status_code=403, detail="Invalid key")

    return await repo.delete_operations()


@admin_router.delete("/meet/all")
async def remove_meets(id: ProtectedIntIDPointer):
    if id.key != ADMIN_TOOLS_KEY:
        raise HTTPException(status_code=403, detail="Invalid key")

    return await repo.delete_meets()
