import unittest
import responses

from zoomus import components, util


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetUserContactsV2TestCase))
    return suite


class GetUserContactsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.contacts.ContactsComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_get_user_contact(self):
        responses.add(responses.GET, "http://foo.com/chat/users/me/contacts/foo")
        self.component.get_user_contact(contact_id="foo")

    def test_requires_id(self):
        with self.assertRaisesRegex(ValueError, "'contact_id' must be set"):
            self.component.get_user_contact()


if __name__ == "__main__":
    unittest.main()
