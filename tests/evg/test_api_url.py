"""Unit tests for url_creator.py"""

import evg.url_creator as under_test


class TestUrlCreator:
    def test_rest_v2_endpoints(self):
        api_server = "evergreen.mongodb.org"
        endpoint = "hello/world"
        creator = under_test.UrlCreator(api_server)

        url = creator.rest_v2(endpoint)

        assert url.startswith(api_server)
        assert url.endswith(endpoint)
        assert "/rest/v2/" in url
