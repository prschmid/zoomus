import unittest
import responses

from zoomus import components, util


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ListUserContactsV2TestCase))
    return suite


class ListUserContactsV2TestCase(unittest.TestCase):
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
    def test_can_list_user_contacts(self):
        responses.add(responses.GET, "http://foo.com/chat/users/me/contacts")
        self.component.list_user_contacts()


if __name__ == "__main__":
    unittest.main()
