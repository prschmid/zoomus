from datetime import datetime
import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ListPanelistsV2TestCase))
    return suite


class ListPanelistsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com", config={"client_id": "CLIENT_ID", "client_secret": "SECRET"}
        )

    @responses.activate
    def test_can_get(self):
        responses.add(responses.GET, "http://foo.com/webinars/42/panelists?id=42")
        self.component.list_panelists(id="42")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.list_panelists()


if __name__ == "__main__":
    unittest.main()
