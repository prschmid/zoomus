import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetV1TestCase))
    return suite


class GetV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponent(
            base_uri="http://foo.com", config={"client_id": "CLIENT_ID", "client_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_get_me(self, mock_get_request):
        self.component.me()
        mock_get_request.assert_called_with("/user/me")


class MeV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponentV2(
            base_uri="http://foo.com", config={"client_id": "CLIENT_ID", "client_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_get_me(self, mock_get_request):
        self.component.me()
        mock_get_request.assert_called_with("/users/me")


if __name__ == "__main__":
    unittest.main()
