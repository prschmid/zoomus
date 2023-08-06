import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteAllAssistantsV2TestCase))
    return suite


class DeleteAllAssistantsV2TestCase(unittest.TestCase):
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
    def test_can_delete_all_assistants(self):
        responses.add(responses.DELETE, "http://foo.com/users/ID/assistants")
        response = self.component.delete_all_assistants(id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.delete_all_assistants()


if __name__ == "__main__":
    unittest.main()
