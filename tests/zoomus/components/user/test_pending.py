import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PendingV1TestCase))
    return suite


class PendingV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.user.UserComponent(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_end(self):
        responses.add(
            responses.POST, "http://foo.com/user/pending?api_key=CLIENT_ID&api_secret=SECRET"
        )
        self.component.pending()


if __name__ == "__main__":
    unittest.main()
