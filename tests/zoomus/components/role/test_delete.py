import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteV2TestCase))
    return suite


class DeleteV2TestCase(unittest.TestCase):
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
    def test_can_delete(self):
        responses.add(responses.DELETE, "http://foo.com/roles/42")
        response = self.component.delete(id="42")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.delete()


if __name__ == "__main__":
    unittest.main()
