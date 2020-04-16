import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CallLogsV2TestCase))
    return suite


class CallLogsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.phone.PhoneComponentV2(
            base_uri="http://example.com",
            config={"api_key": "KEY", "api_secret": "SECRET"},
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_numbers(self, mock_get_request):
        self.component.call_logs()

        mock_get_request.assert_called_with("/phone/call_logs", params={})


if __name__ == "__main__":
    unittest.main()
