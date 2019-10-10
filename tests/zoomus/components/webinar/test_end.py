import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EndV1TestCase))
    return suite


class EndV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_end(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/end?id=ID&host_id=ID&api_key=KEY&api_secret=SECRET",
        )
        self.component.end(id="ID", host_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.end()

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.end(id="ID")


class EndV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_end(self):
        responses.add(responses.PUT, "http://foo.com/webinars/42/status?status=end")
        self.component.end(id="42")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.end()


if __name__ == "__main__":
    unittest.main()
