import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AddAssistantsV2TestCase))
    return suite


class AddAssistantsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_add_assistants(self):
        responses.add(responses.POST, "http://foo.com/users/ID/assistants")
        response = self.component.add_assistants(
            id="ID", assistants=[{"email": "foo@bar.com"}]
        )
        self.assertEqual(
            response.request.body, '{"assistants": [{"email": "foo@bar.com"}]}'
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.add_assistants(assistants=[{"email": "foo@bar.com"}])

    def test_requires_assistants(self):
        with self.assertRaisesRegexp(ValueError, "'assistants' must be set"):
            self.component.add_assistants(id="ID")


if __name__ == "__main__":
    unittest.main()
