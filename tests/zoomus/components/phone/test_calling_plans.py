import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CallingPlansV2TestCase))
    return suite


class CallingPlansV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.phone.PhoneComponentV2(
            base_uri="http://example.com", config={"token": "token"},
        )

    @responses.activate
    def test_numbers(self):
        responses.add(
            responses.GET,
            "http://example.com/phone/calling_plans",
            headers={"Authorization": "Bearer token"},
        )

        self.component.calling_plans()


if __name__ == "__main__":
    unittest.main()
