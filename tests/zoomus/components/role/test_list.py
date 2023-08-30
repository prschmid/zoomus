import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ListV2TestCase))
    return suite


class ListV2TestCase(unittest.TestCase):
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
    def test_can_list(self):
        responses.add(responses.GET, "http://foo.com/roles")
        response = self.component.list()


if __name__ == "__main__":
    unittest.main()
