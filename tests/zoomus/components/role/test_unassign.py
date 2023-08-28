import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnassignV2TestCase))
    return suite


class UnassignV2TestCase(unittest.TestCase):
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
        responses.add(responses.DELETE, "http://foo.com/roles/ID/members/MEMBERID")
        response = self.component.unassign(id="ID", member="MEMBERID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.unassign(member="bar")

    def test_requires_members(self):
        with self.assertRaisesRegexp(ValueError, "'member' must be set"):
            self.component.unassign(id="bar")


if __name__ == "__main__":
    unittest.main()
