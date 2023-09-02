import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetV2TestCase))
    return suite


class GetV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.group.GroupComponentV2(
            base_uri="http://foo.com", config={"client_id": "CLIENT_ID", "client_secret": "SECRET"}
        )

    @responses.activate
    def test_can_get(self):
        responses.add(responses.GET, "http://foo.com/groups/ID")
        self.component.get(id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.get()


if __name__ == "__main__":
    unittest.main()
