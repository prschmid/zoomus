import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateV1TestCase))
    return suite


class UpdateV1TestCase(unittest.TestCase):
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
    def test_can_update(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/update?id=ID&host_id=ID&api_key=KEY&api_secret=SECRET",
        )
        self.component.update(id="ID", host_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update()

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.update(id="ID")

    @responses.activate
    def test_start_time_gets_transformed(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        responses.add(
            responses.POST,
            "http://foo.com/webinar/update?id=42&host_id=HOST"
            "&start_time=1969-01-01T01%3A01%3A00Z&api_key=KEY&api_secret=SECRET",
        )
        self.component.update(id="42", host_id="HOST", start_time=start_time)


class UpdateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_update(self):
        responses.add(responses.PATCH, "http://foo.com/webinars/42")
        response = self.component.update(id="42")
        self.assertEqual(response.request.body, '{"id": "42"}')

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update()


if __name__ == "__main__":
    unittest.main()
