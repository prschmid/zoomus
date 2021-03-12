import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NumbersGetV2TestCase))
    return suite


class NumbersGetV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.phone.PhoneComponentV2(
            base_uri="http://example.com",
            config={"token": "token"},
        )

    @responses.activate
    def test_can_get(self):
        responses.add(
            responses.GET,
            "http://example.com/phone/numbers/ID",
            headers={"Authorization": "Bearer token"},
        )
        self.component.numbers_get(id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.numbers_get()


if __name__ == "__main__":
    unittest.main()
