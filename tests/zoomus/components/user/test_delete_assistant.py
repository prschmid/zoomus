import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteAssistantV2TestCase))
    return suite


class DeleteAssistantV2TestCase(unittest.TestCase):
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
        responses.add(responses.DELETE, "http://foo.com/users/ID/assistants/ASSISTID")
        response = self.component.delete_assistant(
            id="ID", assistant_id="ASSISTID"
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.delete_assistant(assistant_id="ASSISTID")

    def test_requires_assistant_id(self):
        with self.assertRaisesRegexp(ValueError, "'assistant_id' must be set"):
            self.component.delete_assistant(id="ID")


if __name__ == "__main__":
    unittest.main()
