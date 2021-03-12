import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateV1TestCase))
    suite.addTest(unittest.makeSuite(CreateV2TestCase))
    return suite


class CreateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.group.GroupComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_create(self):
        responses.add(responses.POST, "http://foo.com/groups")
        response = self.component.create(name="bar")
        self.assertEqual(response.request.body, '{"name": "bar"}')

    def test_requires_name(self):
        with self.assertRaisesRegexp(ValueError, "'name' must be set"):
            self.component.create()


if __name__ == "__main__":
    unittest.main()
