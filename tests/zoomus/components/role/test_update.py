import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UpdateV2TestCase))
    return suite


def update(self, **kwargs):
    util.require_keys(kwargs, ["id", "name", "description", "privileges"])

    return self.patch_request("/roles/{}".format(kwargs.pop("id")), data=kwargs)


class UpdateV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.role.RoleComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_create(self):
        responses.add(responses.PATCH, "http://foo.com/roles/ID")
        response = self.component.update(
            id="ID", name="bar", description="bar", privileges=["foo", "bar"]
        )
        self.assertEqual(
            response.request.body,
            '{"name": "bar", "description": "bar", "privileges": ["foo", "bar"]}',
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.update(
                name="bar", description="bar", privileges=["foo", "bar"]
            )

    def test_requires_name(self):
        with self.assertRaisesRegexp(ValueError, "'name' must be set"):
            self.component.update(id="ID", description="bar", privileges=["foo", "bar"])

    def test_requires_description(self):
        with self.assertRaisesRegexp(ValueError, "'description' must be set"):
            self.component.update(id="ID", name="bar", privileges=["foo", "bar"])

    def test_requires_privileges(self):
        with self.assertRaisesRegexp(ValueError, "'privileges' must be set"):
            self.component.update(id="ID", name="bar", description="bar")


if __name__ == "__main__":
    unittest.main()
