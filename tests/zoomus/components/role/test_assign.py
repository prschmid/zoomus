import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssignV2TestCase))
    return suite


class AssignV2TestCase(unittest.TestCase):
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
    def test_can_assign(self):
        responses.add(responses.POST, "http://foo.com/roles/ID/members")
        response = self.component.assign(
            id="ID", members=["test1@example.com", "test2@example.com"]
        )
        self.assertEqual(
            response.request.body,
            '{"members": ["test1@example.com", "test2@example.com"]}',
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.assign(members=["bar"])

    def test_requires_members(self):
        with self.assertRaisesRegexp(ValueError, "'members' must be set"):
            self.component.assign(id="foo")


if __name__ == "__main__":
    unittest.main()
