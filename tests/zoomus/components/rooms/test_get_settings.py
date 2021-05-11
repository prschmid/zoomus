import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetSettingsV2TestCase))
    return suite


class GetSettingsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.room.RoomComponentV2(
            base_uri="http://foo.com",
            config={
                "token": "token",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_get_settings(self):
        responses.add(
            responses.GET, "http://foo.com/rooms/42/settings?setting_type=meeting"
        )
        self.component.get_settings(id="42", setting_type="meeting")

    def test_requires_setting_type(self):
        with self.assertRaisesRegexp(ValueError, "'setting_type' must be set"):
            self.component.get_settings(id="42")

    def test_requires_room_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.get_settings()


if __name__ == "__main__":
    unittest.main()
