import unittest
import responses

from zoomus import components, util


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SearchV2TestCase))
    return suite


class SearchV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.contacts.ContactsComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_search(self):
        responses.add(responses.GET, "http://foo.com/contacts")
        self.component.search(search_key='foo')

    def test_requires_id(self):
        with self.assertRaisesRegex(ValueError, "'search_key' must be set"):
            self.component.search()


if __name__ == "__main__":
    unittest.main()
