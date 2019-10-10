import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteV1TestCase))
    return suite


class DeleteV1TestCase(unittest.TestCase):
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
    def test_can_delete(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/delete?id=ID&host_id=ID&api_key=KEY&api_secret=SECRET",
        )
        self.component.delete(id="ID", host_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.delete()

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.delete(id="ID")


class DeleteV2TestCase(unittest.TestCase):
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
    def test_can_delete(self):
        responses.add(responses.DELETE, "http://foo.com/webinars/42?id=42")
        self.component.delete(id="42")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.delete()


if __name__ == "__main__":
    unittest.main()
