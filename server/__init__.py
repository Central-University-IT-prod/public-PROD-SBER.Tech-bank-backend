from server.db.repo import Repo
from server.config import DISABLE_DATABASE

if not DISABLE_DATABASE:
    from server.db.settings import async_session

    repo = Repo(async_session)  # type: ignore
else:
    repo = Repo
