import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateSettingsV2TestCase))
    return suite


class UpdateSettingsV2TestCase(unittest.TestCase):
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
    def test_can_update_settings(self):
        responses.add(responses.PATCH, "http://foo.com/users/42/settings")
        response = self.component.update_settings(id="42", schedule_meeting="foo")
        self.assertEqual(response.request.body, '{"schedule_meeting": "foo"}')

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update_settings()


if __name__ == "__main__":
    unittest.main()
