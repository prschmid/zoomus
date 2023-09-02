import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetByEmailV1TestCase))
    return suite


class GetByEmailV1TestCase(unittest.TestCase):
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
    def test_can_get_by_email(self):
        responses.add(
            responses.POST,
            "http://foo.com/user/getbyemail?email=a@b.com&login_type=foo&api_key=CLIENT_ID&api_secret=SECRET",
        )
        self.component.get_by_email(email="a@b.com", login_type="foo")

    def test_requires_email(self):
        with self.assertRaisesRegexp(ValueError, "'email' must be set"):
            self.component.get_by_email()

    def test_requires_login_type(self):
        with self.assertRaisesRegexp(ValueError, "'login_type' must be set"):
            self.component.get_by_email(email="a@b.com")


if __name__ == "__main__":
    unittest.main()
