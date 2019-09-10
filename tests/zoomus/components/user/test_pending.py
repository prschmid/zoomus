import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PendingV1TestCase))
    return suite


class PendingV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    def test_can_end(self):
        with patch.object(
            components.base.BaseComponent, "post_request", return_value=True
        ) as mock_post_request:

            self.component.pending()

            mock_post_request.assert_called_with("/user/pending", params={})


if __name__ == "__main__":
    unittest.main()
