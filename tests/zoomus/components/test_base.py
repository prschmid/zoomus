import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from zoomus import API_VERSION_1, API_VERSION_2, components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseComponentTestCase))
    return suite


@mock.patch("zoomus.components.base.util.ApiClient.post_request")
class BaseComponentTestCase(unittest.TestCase):
    def test_post_request_includes_config_details_in_data_when_no_data(
        self, mock_post_request
    ):
        component = components.base.BaseComponent(
            base_uri="http://www.foo.com",
            config={"api_key": "KEY", "api_secret": "SECRET", "version": API_VERSION_1},
        )
        component.post_request("foo")
        mock_post_request.assert_called_with(
            "foo", params=component.config, data=None, headers=None, cookies=None
        )

    def test_post_request_includes_config_details_in_data_when_there_is_data(
        self, mock_post_request
    ):
        component = components.base.BaseComponent(
            base_uri="http://www.foo.com",
            config={"api_key": "KEY", "api_secret": "SECRET", "version": API_VERSION_1},
        )
        component.post_request("foo", params={"foo": "bar"})

        params = {"foo": "bar"}
        params.update(component.config)

        mock_post_request.assert_called_with(
            "foo", params=params, data=None, headers=None, cookies=None
        )

    def test_v2_post_request_passes_jwt_token(self, mock_post_request):
        component = components.base.BaseComponent(
            base_uri="http://www.foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": API_VERSION_2,
                "token": 42,
            },
        )
        component.post_request("foo")
        mock_post_request.assert_called_with(
            "foo",
            params={},
            data=None,
            headers={"Authorization": "Bearer 42"},
            cookies=None,
        )


if __name__ == "__main__":
    unittest.main()
