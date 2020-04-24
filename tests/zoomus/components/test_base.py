import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseComponentTestCase))
    return suite


class BaseComponentTestCase(unittest.TestCase):
    @responses.activate
    def test_post_request_includes_config_details_in_data_when_no_data(self):
        component = components.base.BaseComponent(
            base_uri="http://www.foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )
        responses.add(
            responses.POST, "http://www.foo.com/foo?api_key=KEY&api_secret=SECRET"
        )
        component.post_request("foo")

    @responses.activate
    def test_post_request_includes_config_details_in_data_when_there_is_data(self):
        component = components.base.BaseComponent(
            base_uri="http://www.foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )
        responses.add(
            responses.POST,
            "http://www.foo.com/foo?foo=bar&api_key=KEY&api_secret=SECRET",
        )
        component.post_request("foo", params={"foo": "bar"})

    @responses.activate
    def test_v2_post_request_passes_jwt_token(self):
        component = components.base.BaseComponent(
            base_uri="http://www.foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
                "token": 42,
            },
        )
        responses.add(
            responses.POST,
            "http://www.foo.com/foo",
            headers={"Authorization": "Bearer 42"},
        )
        component.post_request("foo")


if __name__ == "__main__":
    unittest.main()
