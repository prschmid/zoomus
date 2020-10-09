from datetime import datetime
import unittest

from zoomus import components
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AddPanelistsV2TestCase))
    return suite


class AddPanelistsV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

   @responses.activate
    def test_can_add_panelists(self):
        responses.add(
            responses.POST, "http://foo.com/webinar/ID/panelists",
        )
        response = self.component.add_panelists(panelists=[{"name": "Mary", "email": "maryjkdfdsgfshdgf@jdfdkjdglfk.jkfgdj"}])
        self.assertEqual(
            response.request.body, '{panelists: [{"name": "Mary", "email": "maryjkdfdsgfshdgf@jdfdkjdglfk.jkfgdj"}]}'
        )

    def test_requires_panelists(self):
        with self.assertRaisesRegexp(ValueError, "'panelists' must be set"):
            self.component.add_panelists()    


if __name__ == "__main__":
    unittest.main()
