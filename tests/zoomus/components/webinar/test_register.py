import datetime
import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RegisterV1TestCase))
    suite.addTest(unittest.makeSuite(RegisterV2TestCase))
    return suite


class RegisterV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_register(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinar/register?id=ID&email=foo@bar.com&first_name=Foo&last_name=Bar"
            "&api_key=CLIENT_ID&api_secret=SECRET",
        )
        self.component.register(
            id="ID", email="foo@bar.com", first_name="Foo", last_name="Bar"
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

    @responses.activate
    def test_start_time_gets_transformed(self):
        start_time = datetime.datetime(1969, 1, 1, 1, 1)
        responses.add(
            responses.POST,
            "http://foo.com/webinar/register?id=ID&email=foo@bar.com&first_name=foo&last_name=bar"
            "&start_time=1969-01-01T01%3A01%3A00Z&api_key=CLIENT_ID&api_secret=SECRET",
        )
        self.component.register(
            id="ID",
            email="foo@bar.com",
            first_name="foo",
            last_name="bar",
            start_time=start_time,
        )


class RegisterV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.webinar.WebinarComponentV2(
            base_uri="http://foo.com",
            config={
                "client_id": "CLIENT_ID",
                "client_secret": "SECRET",
                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_register(self):
        responses.add(
            responses.POST,
            "http://foo.com/webinars/42/registrants",
        )
        response = self.component.register(
            id="42", email="foo@bar.com", first_name="Foo", last_name="Bar"
        )
        self.assertEqual(
            response.request.body,
            '{"id": "42", "email": "foo@bar.com", "first_name": "Foo", "last_name": "Bar"}',
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
