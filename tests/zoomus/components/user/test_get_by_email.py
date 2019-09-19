import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetByEmailV1TestCase))
    return suite


class GetByEmailV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    def test_can_get_by_email(self):
        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            self.component.get_by_email(email="a@b.com", login_type="foo")

            mock_post_request.assert_called_with(
                "/user/getbyemail", params={"email": "a@b.com", "login_type": "foo"}
            )

    def test_requires_email(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_by_email()
            self.assertEqual(context.exception.message, "'email' must be set")

    def test_requires_login_type(self):
        with self.assertRaises(ValueError) as context:
            self.component.get_by_email()
            self.assertEqual(context.exception.message, "'login_type' must be set")


if __name__ == "__main__":
    unittest.main()
