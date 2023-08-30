import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CustCreateV1TestCase))
    return suite


class CustCreateV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponent(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_create_by_email(self):
        responses.add(
            responses.POST,
            "http://foo.com/user/custcreate?type=foo&email=a@b.com&api_key=CLIENT_ID&api_secret=SECRET",
        )
        self.component.cust_create(type="foo", email="a@b.com")

    def test_requires_type(self):
        with self.assertRaisesRegexp(ValueError, "'type' must be set"):
            self.component.cust_create()

    def test_requires_email(self):
        with self.assertRaisesRegexp(ValueError, "'email' must be set"):
            self.component.cust_create(type="foo")


if __name__ == "__main__":
    unittest.main()
