"""Async API client for Evergreen."""
from contextlib import asynccontextmanager
from typing import Dict, Any, Generator, NamedTuple, Optional, Iterable

from aiohttp import ClientSession

from evg.config import EvgAuth
from evg.models.build import EvgBuild
from evg.models.evg_task import EvgTask

DEFAULT_LIMIT = 100


class EvgApiConfig(NamedTuple):

    api_server: str
    auth: EvgAuth
    timeout: Optional[int] = None


class EvergreenApi(object):

    def __init__(self, api_server: str, timeout: int, session: ClientSession) -> None:
        self.api_server = api_server
        self.session = session
        self.timeout = timeout

    async def _call_api(self, url: str, params: Optional[Dict[str, Any]]) -> Dict:
        response = self.session.get(url=url, params=params)
        response.raise_for_status()

        return await response

    async def _call_api_json(self, url: str, params: Optional[Dict[str, Any]]) -> Dict:
        response = self._call_api(url, params)
        return await response.json()

    async def _paginate(self, url: str, params: Optional[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
        if not params:
            params = {"limit": DEFAULT_LIMIT}
        
        next_url = url
        while True:
            response = await self._call_api(next_url, params)
            json_response = await response.json()
            if not json_response:
                break

            for result in json_response:
                yield result

            if "next" not in response.links:
                break

            next_url = response.links["next"]["url"]
        
    
    def build_v2_api(self, endpoint: str) -> str:
        return f"{self.api_server}/rest/v2/{endpoint}"

    async def build_by_id(self, build_id: str) -> EvgBuild:
        endpoint = self.build_v2_api(f"/builds/{build_id}")
        response = await self._call_api_json(endpoint)

        return EvgBuild(**response)

    async def tasks_by_build(self, build_id: str, fetch_all_executions: Optional[bool] = None) -> Iterable[EvgTask]:
        params = {}
        if fetch_all_executions:
            params["fetch_all_executions"] = 1

        endpoint = self.build_v2_api(f"/builds/{build_id}/tasks")
        response = self._paginate(endpoint, params)
        return (EvgTask(**task) for task in response)


@asynccontextmanager
async def EvergreenApiSession(evg_config: EvgApiConfig) -> Generator[EvergreenApi, None, None]:
    async with ClientSession(headers=evg_config.auth.auth_headers) as session:
        evg_api = EvergreenApi(evg_config.api_server, evg_config.timeout, session)
        yield evg_api

