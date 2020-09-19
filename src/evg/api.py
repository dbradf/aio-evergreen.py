"""Async API client for Evergreen."""
from contextlib import asynccontextmanager
from typing import Dict, Any, Generator, NamedTuple, Optional, Iterable, AsyncIterable

from aiohttp import ClientSession, ClientResponse

from evg.config import EvgAuth
from evg.models.build import EvgBuild
from evg.models.evg_patch import EvgPatch
from evg.models.evg_task import EvgTask
from evg.models.evg_version import EvgVersion

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

    async def _call_api(self, url: str, params: Optional[Dict[str, Any]]) -> ClientResponse:
        response = await self.session.get(url=url, params=params)
        response.raise_for_status()

        return response

    async def _call_api_json(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        response = await self._call_api(url, params)
        return await response.json()

    async def _paginate(self, url: str, params: Optional[Dict[str, Any]] = None) -> AsyncIterable[Dict[str, Any]]:
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

    async def version_by_id(self, version_id: str) -> EvgVersion:
        endpoint = self.build_v2_api(f"/versions/{version_id}")
        response = await self._call_api_json(endpoint)

        return EvgVersion(**response)

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
        return (EvgTask(**task) async for task in response)

    async def user_patches(self, user_id: str) -> Generator[EvgPatch, None, None]:
        endpoint = self.build_v2_api(f"/users/{user_id}/patches")
        responses = self._paginate(endpoint)

        return (EvgPatch(**patch) async for patch in responses)


@asynccontextmanager
async def EvergreenApiSession(evg_config: EvgApiConfig) -> Generator[EvergreenApi, None, None]:
    async with ClientSession(headers=evg_config.auth.auth_headers()) as session:
        evg_api = EvergreenApi(evg_config.api_server, evg_config.timeout, session)
        yield evg_api

