from datetime import datetime
import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AbsenteesV2TestCase))
    return suite


class AbsenteesV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @responses.activate
    def test_can_absentees(self):
        responses.add(responses.GET, "http://foo.com/past_webinars/ID/absentees?id=ID")
        self.component.get_absentees(id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.get()


if __name__ == "__main__":
    unittest.main()
