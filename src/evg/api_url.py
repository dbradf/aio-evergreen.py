"""URL creator for the evergreen API."""


class UrlCreator:
    """Class to create evergreen URLs."""

    def __init__(self, api_server: str) -> None:
        """
        Initialize a url creator.

        :param api_server: Hostname API server to connect to.
        """
        self.api_server = api_server

    def rest_v2(self, endpoint: str) -> str:
        """
        Create a REST V2 url.

        :param endpoint: Endpoint to connect to.
        :return: URL to access given endpoint.
        """
        return f"{self.api_server}/rest/v2/{endpoint}"
