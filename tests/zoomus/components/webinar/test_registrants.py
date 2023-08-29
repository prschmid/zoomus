from datetime import datetime
import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RegisterantsV2TestCase))
    return suite


class RegisterantsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com", config={"client_id": "CLIENT_ID", "client_secret": "SECRET"}
        )

    @responses.activate
    def test_can_registrants(self):
        responses.add(responses.GET, "http://foo.com/webinars/ID/registrants?id=ID")
        self.component.get_registrants(id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.get()


if __name__ == "__main__":
    unittest.main()
