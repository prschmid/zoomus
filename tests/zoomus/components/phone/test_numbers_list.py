import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NumbersListV2TestCase))
    return suite


class NumbersListV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.phone.PhoneComponentV2(
            base_uri="http://example.com",
            config={"token": "token"},
        )

    @responses.activate
    def test_numbers(self):
        responses.add(
            responses.GET,
            "http://example.com/phone/numbers",
            headers={"Authorization": "Bearer token"},
        )
        self.component.numbers_list()


if __name__ == "__main__":
    unittest.main()
