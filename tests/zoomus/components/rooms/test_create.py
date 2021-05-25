import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateV2TestCase))
    return suite


class CreateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.room.RoomComponentV2(
            base_uri="http://foo.com",
            config={
                "token": "token",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_create(self):
        responses.add(responses.POST, "http://foo.com/rooms")
        response = self.component.create(name="bar", type="foo")
        self.assertEqual(response.request.body, '{"name": "bar", "type": "foo"}')

    def test_requires_type(self):
        with self.assertRaisesRegexp(ValueError, "'type' must be set"):
            self.component.create(name="bar")

    def test_requires_name(self):
        with self.assertRaisesRegexp(ValueError, "'name' must be set"):
            self.component.create()


if __name__ == "__main__":
    unittest.main()
