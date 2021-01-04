"""Async version of the evergreen API."""
import asyncio
from typing import Any, AsyncIterable, Callable, Dict, List, NamedTuple, Optional, TypeVar

from aiohttp import ClientResponse, ClientSession

from evg.api_requests import StatsSpecification
from evg.models.evg_manifest import EvgManifest
from evg.models.evg_patch import EvgPatch
from evg.models.evg_project import EvgProject
from evg.models.evg_stats import EvgTaskStats, EvgTestStats
from evg.models.evg_task import EvgTask
from evg.models.evg_version import EvgVersion, Requester
from evg.url_creator import UrlCreator

T = TypeVar("T")


class _ResponseData(NamedTuple):
    """
    Response from a paginated HTTP call.

    json_data: List of returned data.
    next_link: Link to next batch of data.
    """

    json_data: List[Dict[str, Any]]
    next_link: Optional[str]


def _get_next_url(response: ClientResponse) -> Optional[str]:
    """
    Get the link to the next batch of paginated data.

    :param response: HTTP response.
    :return: Link to next batch of data if it exists.
    """
    next_link = response.links.get("next")
    if next_link:
        return str(next_link["url"])
    return None


class AioEvergreenApi:
    """Async evergreen API object."""

    def __init__(self, session: ClientSession, api_server: str) -> None:
        """
        Initialize the Evergreen API Client.

        :param session: HTTP session to use.
        :param api_server: API server to make queries to.
        """
        self.session: Optional[ClientSession] = session
        self.url_creator = UrlCreator(api_server)

    def close(self) -> None:
        """Close the session this API client was using."""
        self.session = None

    async def _make_get_request(self, url: str, params: Optional[Dict[str, Any]]) -> _ResponseData:
        """
        Make a GET request.

        :param url: URL to make request to.
        :param params: Params to send to URL.
        :return: Response from GET request.
        """
        if self.session is None:
            return _ResponseData([], None)

        async with self.session.get(url, params=params) as resp:
            resp.raise_for_status()
            return _ResponseData(await resp.json(), _get_next_url(resp))

    async def _response_iterator(
        self,
        url: str,
        transform_fn: Callable[[Dict[str, Any]], T],
        params: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterable[T]:
        response = await self._make_get_request(url, params)
        while True:
            if not response.json_data:
                break

            next_response = None
            if response.next_link:
                next_response = asyncio.create_task(
                    self._make_get_request(response.next_link, params)
                )

            for item in response.json_data:
                yield transform_fn(item)

            if next_response:
                response = await next_response
            else:
                break

    # Projects

    async def all_project(self) -> AsyncIterable[EvgProject]:
        """Get an iterable over all evergreen projects."""
        url = self.url_creator.rest_v2("projects")
        return self._response_iterator(url, transform_fn=lambda d: EvgProject(**d))

    # Versions

    async def versions_by_project(
        self, project_id: str, requester: Requester = Requester.GITTER_REQUEST
    ) -> AsyncIterable[EvgVersion]:
        """
        Get an iterable over the versions of a given project.

        :param project_id: ID of project to query.
        :param requester: Iterate of version created by this requester type.
        :return: Iterable over versions.
        """
        url = self.url_creator.rest_v2(f"projects/{project_id}/versions")
        params = {"requester": requester.evg_value()}
        return self._response_iterator(url, lambda v: EvgVersion(**v), params)

    # Patches

    async def patches_by_project(self, project_id: str) -> AsyncIterable[EvgPatch]:
        """
        Get an iterable over the patches for a given projects.

        :param project_id: ID of project to query.
        :return: Iterable over patches.
        """
        url = self.url_creator.rest_v2(f"projects/{project_id}/patches")
        return self._response_iterator(url, lambda p: EvgPatch(**p))

    async def patches_by_user(self, user_id: str) -> AsyncIterable[EvgPatch]:
        """
        Get an iterable over the patches submitted by a user.

        :param user_id: ID of user to query.
        :return: Iterable over patches.
        """
        url = self.url_creator.rest_v2(f"users/{user_id}/patches")
        return self._response_iterator(url, lambda p: EvgPatch(**p))

    # Tasks

    async def task_by_id(self, task_id: str) -> EvgTask:
        """
        Get a task by its ID.

        :param task_id: ID of task to query.
        :return: Data about the task.
        """
        url = self.url_creator.rest_v2(f"tasks/{task_id}")
        with self.session.get(url) as response:
            response.raise_for_status()
            return EvgTask(**await response.json())

    async def tasks_by_build(self, build_id: str) -> AsyncIterable[EvgTask]:
        """
        Get an iterable over all tasks for the specified build.

        :param build_id: ID of build to query.
        :return: Iterable over tasks.
        """
        url = self.url_creator.rest_v2(f"builds/{build_id}/tasks")
        return self._response_iterator(url, lambda t: EvgTask(**t))

    async def tasks_by_project_and_commit(
        self, project_id: str, revision: str
    ) -> AsyncIterable[EvgTask]:
        """
        Get an iterable over all tasks for git commit and project.

        :param project_id: ID of project to query.
        :param revision: Git commit to query.
        :return: Iterable over tasks.
        """
        url = self.url_creator.rest_v2(f"projects/{project_id}/revisions/{revision}/tasks")
        return self._response_iterator(url, lambda t: EvgTask(**t))

    async def manifest_for_task(self, task_id: str) -> EvgManifest:
        """
        Get the manifest for the specified task.

        :param task_id: ID of task to query.
        :return: Manifest for specified task.
        """
        url = self.url_creator.rest_v2(f"tasks/{task_id}/manifest")
        with self.session.get(url) as response:
            response.raise_for_status()
            return EvgManifest(**await response.json())

    # Stats

    async def test_stats(self, stats_spec: StatsSpecification) -> AsyncIterable[EvgTestStats]:
        """
        Get an iterable of test stats for the given specification.

        :param stats_spec: Specification of which tests to query.
        :return: Iterable of test stats.
        """
        params = stats_spec.get_params()
        url = self.url_creator.rest_v2(f"projects/{stats_spec.project_id}/test_stats")
        return self._response_iterator(url, lambda s: EvgTestStats(**s), params=params)

    async def task_stats(self, stats_spec: StatsSpecification) -> AsyncIterable[EvgTaskStats]:
        """
        Get an iterable of task stats for the given specification.

        :param stats_spec: Specification of which tasks to query.
        :return: Iterable of tasks stats.
        """
        params = stats_spec.get_params()
        url = self.url_creator.rest_v2(f"projects/{stats_spec.project_id}/task_stats")
        return self._response_iterator(url, lambda s: EvgTaskStats(**s), params=params)
