import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DeleteV1TestCase))
    return suite


class DeleteV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.recording.RecordingComponent(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_delete(self):
        responses.add(
            responses.POST,
            "http://foo.com/recording/delete?meeting_id=ID&api_key=KEY&api_secret=SECRET",
        )
        self.component.delete(meeting_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.delete()


class DeleteV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.recording.RecordingComponentV2(
            base_uri="http://foo.com",
            config={
                "api_key": "KEY",
                "api_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_delete(self):
        responses.add(
            responses.DELETE, "http://foo.com/meetings/42/recordings?meeting_id=42"
        )
        self.component.delete(meeting_id="42")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'meeting_id' must be set"):
            self.component.delete()


if __name__ == "__main__":
    unittest.main()
