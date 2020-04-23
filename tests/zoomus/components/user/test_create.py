import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateV1TestCase))
    return suite


class CreateV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponent(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_create(self):
        responses.add(responses.POST, "http://foo.com/user/create")
        self.component.create()


class CreateV2TestCase(unittest.TestCase):
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
    def test_can_create(self):
        responses.add(responses.POST, "http://foo.com/users")
        response = self.component.create(foo="bar")
        self.assertEqual(response.request.body, '{"foo": "bar"}')


if __name__ == "__main__":
    unittest.main()
