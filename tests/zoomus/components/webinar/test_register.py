from datetime import datetime
import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import components


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RegisterV1TestCase))
    return suite


class RegisterV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_can_register(self, mock_post_request):
        self.component.register(
            id="ID", email="foo@bar.com", first_name="Foo", last_name="Bar"
        )

        mock_post_request.assert_called_with(
            "/webinar/register",
            params={
                "id": "ID",
                "email": "foo@bar.com",
                "first_name": "Foo",
                "last_name": "Bar",
            },
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.register()

    def test_requires_email(self):
        with self.assertRaisesRegexp(ValueError, "'email' must be set"):
            self.component.register(id="ID")

    def test_requires_first_name(self):
        with self.assertRaisesRegexp(ValueError, "'first_name' must be set"):
            self.component.register(id="ID", email="foo@bar.com")

    def test_requires_last_name(self):
        with self.assertRaisesRegexp(ValueError, "'last_name' must be set"):
            self.component.register(id="ID", email="foo@bar.com", first_name="foo")

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_start_time_gets_transformed(self, mock_post_request):
        self.component.register(
            id="ID",
            email="foo@bar.com",
            first_name="foo",
            last_name="bar",
            start_time=datetime(1969, 1, 1),
        )
        mock_post_request.assert_called_with(
            "/webinar/register",
            params={
                "id": "ID",
                "email": "foo@bar.com",
                "first_name": "foo",
                "last_name": "bar",
                "start_time": "1969-01-01T00:00:00Z",
            },
        )


class RegisterV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com", config={"api_key": "KEY", "api_secret": "SECRET"}
        )

    @patch.object(components.base.BaseComponent, "post_request", return_value=True)
    def test_can_register(self, mock_post_request):
        self.component.register(
            id="ID", email="foo@bar.com", first_name="Foo", last_name="Bar"
        )

        mock_post_request.assert_called_with(
            "/webinars/ID/registrants",
            params={
                "id": "ID",
                "email": "foo@bar.com",
                "first_name": "Foo",
                "last_name": "Bar",
            },
        )

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.register()

    def test_requires_email(self):
        with self.assertRaisesRegexp(ValueError, "'email' must be set"):
            self.component.register(id="ID")

    def test_requires_first_name(self):
        with self.assertRaisesRegexp(ValueError, "'first_name' must be set"):
            self.component.register(id="ID", email="foo@bar.com")

    def test_requires_last_name(self):
        with self.assertRaisesRegexp(ValueError, "'last_name' must be set"):
            self.component.register(id="ID", email="foo@bar.com", first_name="foo")


if __name__ == "__main__":
    unittest.main()
