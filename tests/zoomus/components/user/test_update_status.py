import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateStatusV2TestCase))
    return suite


class UpdateStatusV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_update_update(self):
        responses.add(responses.PUT, "http://foo.com/users/42/status")
        response = self.component.update_status(id="42", action="activate")
        self.assertEqual(response.request.body, '{"action": "activate"}')

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update_status()

    def test_requires_action(self):
        with self.assertRaisesRegexp(ValueError, "'action' must be set"):
            self.component.update_status(id="42")


if __name__ == "__main__":
    unittest.main()
