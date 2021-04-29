import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteV2TestCase))
    return suite


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
    def test_can_delete_panelists(self):
        responses.add(
            responses.DELETE,
            "http://foo.com/webinars/ID/panelists",
        )
        response = self.component.remove_panelists(id="ID")
        self.assertEqual(response.request.body, None)

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.remove_panelists()


if __name__ == "__main__":
    unittest.main()
