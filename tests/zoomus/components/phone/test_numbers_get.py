import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NumbersGetV2TestCase))
    return suite


class NumbersGetV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.phone.PhoneComponentV2(
            base_uri="http://example.com",
            config={"api_key": "KEY", "api_secret": "SECRET"},
        )

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_numbers(self, mock_get_request):
        self.component.numbers_list()

        mock_get_request.assert_called_with("/phone/numbers", params={})

    @patch.object(components.base.BaseComponent, "get_request", return_value=True)
    def test_can_get(self, mock_get_request):
        self.component.numbers_get(id="ID")
        mock_get_request.assert_called_with("/phone/numbers/ID", params={"id": "ID"})

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.numbers_get()


if __name__ == "__main__":
    unittest.main()
