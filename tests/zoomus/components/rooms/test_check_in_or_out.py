import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CheckInOrOutV2TestCase))
    return suite


class CheckInOrOutV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.room.RoomComponentV2(
            base_uri="http://foo.com",
            config={
                "token": "token",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_check_in_or_out(self):
        responses.add(responses.PATCH, "http://foo.com/rooms/42/events")
        response = self.component.check_in_or_out(id="42")
        self.assertEqual(response.request.body, '{"id": "42"}')

    def test_requires_room_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update()


if __name__ == "__main__":
    unittest.main()
