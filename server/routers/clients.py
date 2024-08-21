from typing import Any

from fastapi import APIRouter

from server import repo
from server.schemas import ClientSchema

client_router = APIRouter()


@client_router.get("/client/{id}", response_model=ClientSchema)
async def get_client(id: Any):
    return {
        "id": id,
        "name": "ПАО СберТех",
        "logo_url": "https://media.licdn.com/dms/image/D4E0BAQHjJIhwoTSFXw/company-logo_200_200/0/1699448612599/sberbank_technology_logo?e=2147483647&v=beta&t=S7U82kxIW6aD6OXRTrg77i-ggH1BO3deUf7dNfWopO0",
    }  # FIXME: Change hardcoded MVP values
