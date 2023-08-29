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
        self.component = components.role.RoleComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_create(self):
        responses.add(responses.POST, "http://foo.com/roles")
        response = self.component.create(
            name="bar", description="bar", privileges=["foo", "bar"], type="iq"
        )
        self.assertEqual(
            response.request.body,
            '{"name": "bar", "description": "bar", "privileges": ["foo", "bar"], "type": "iq"}',
        )

    @responses.activate
    def test_can_create_no_type(self):
        responses.add(responses.POST, "http://foo.com/roles")
        response = self.component.create(
            name="bar", description="bar", privileges=["foo", "bar"]
        )
        self.assertEqual(
            response.request.body,
            '{"name": "bar", "description": "bar", "privileges": ["foo", "bar"], "type": "common"}',
        )

    def test_requires_name(self):
        with self.assertRaisesRegexp(ValueError, "'name' must be set"):
            self.component.create(description="bar", privileges=["foo", "bar"])

    def test_requires_description(self):
        with self.assertRaisesRegexp(ValueError, "'description' must be set"):
            self.component.create(name="bar", privileges=["foo", "bar"])

    def test_requires_privileges(self):
        with self.assertRaisesRegexp(ValueError, "'privileges' must be set"):
            self.component.create(name="bar", description="bar")


if __name__ == "__main__":
    unittest.main()
