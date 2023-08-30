import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EndV1TestCase))
    suite.addTest(unittest.makeSuite(EndV2TestCase))
    return suite


class EndV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_end(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/end?id=ID&host_id=ID&api_key=CLIENT_ID&api_secret=SECRET",
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
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_end(self):
        responses.add(responses.PUT, "http://foo.com/webinars/42/status")
        response = self.component.end(id="42")
        self.assertEqual(response.request.body, '{"status": "end"}')

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.end()


if __name__ == "__main__":
    unittest.main()
