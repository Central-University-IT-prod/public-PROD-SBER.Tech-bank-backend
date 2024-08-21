from fastapi import APIRouter, HTTPException

from server import repo
from server.schemas import OperationSchema, OperationsRequestSchema

operations_router = APIRouter()


@operations_router.get("/operation/{id}", response_model=OperationSchema)
async def get_operation(id: int):
    operation = await repo.get_operation_by_id(id)

    if not operation:
        raise HTTPException(status_code=404, detail=f"Operation with id {id} not found")

    return operation


@operations_router.get("/fetch_operations/", response_model=dict[int, OperationSchema])
async def get_operations_by_ids(ids: OperationsRequestSchema):
    operations = await repo.get_operations_by_ids(ids.ids)
    return {id: operation for id, operation in enumerate(operations)}


@operations_router.get("/fetch_documents_for_operations/", response_model=list[str])
async def get_documents(ids: OperationsRequestSchema):
    operations = await repo.get_operations_by_ids(ids.ids)

    documents = set()
    for operation in operations:
        for doc in operation.documents:
            documents.add(doc.lower().capitalize())

    return list(documents)


@operations_router.get("/operations/", response_model=list[OperationSchema])
async def get_operations():
    operations = await repo.get_all_operations()

    return operations
