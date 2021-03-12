import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParticipantsV2TestCase))
    return suite


class MembersV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.group.GroupComponentV2(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )

    @responses.activate
    def test_can_list(self):
        responses.add(
            responses.GET,
            "http://www.foo.com/groups/ID/members",
        )
        self.component.list_members(groupid="ID")
        expected_headers = {"Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    def test_requires_group_id(self):
        with self.assertRaisesRegexp(ValueError, "'groupid' must be set"):
            self.component.list_members()


if __name__ == "__main__":
    unittest.main()
