from datetime import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AddPanelistsV2TestCase))
    return suite


class AddPanelistsV2TestCase(unittest.TestCase):
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
    def test_can_add_panelists(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinars/ID/panelists",
        )
        response = self.component.add_panelists(
            id="ID", panelists=[{"name": "Mary", "email": "test@test.com"}]
        )
        self.assertEqual(
            response.request.body,
            '{"id": "ID", "panelists": [{"name": "Mary", "email": "test@test.com"}]}',
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.add_panelists()


if __name__ == "__main__":
    unittest.main()
