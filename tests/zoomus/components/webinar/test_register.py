import datetime
import unittest

from mock import patch

from zoomus import (
    components,
    util)


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RegisterTestCase))
    return suite


class RegisterTestCase(unittest.TestCase):

    def setUp(self):
        self.component = components.webinar.WebinarComponent(
            base_uri="http://foo.com",
            config={
                'api_key': 'KEY',
                'api_secret': 'SECRET'
            }
        )

    def test_can_register(self):
        with patch.object(components.base.BaseComponent, 'post_request',
                          return_value=True) as mock_post_request:

            self.component.register(
                id='ID',
                email='foo@bar.com',
                first_name="Foo",
                last_name="Bar")

            mock_post_request.assert_called_with(
                "/webinar/register",
                params={
                    'id': 'ID',
                    'email': 'foo@bar.com',
                    'first_name': 'Foo',
                    'last_name': 'Bar'
                }
            )

    def test_requires_id(self):
        with self.assertRaises(ValueError) as context:
            self.component.create()
            self.assertEqual(
                context.exception.message, "'id' must be set")

    def test_requires_email(self):
        with self.assertRaises(ValueError) as context:
            self.component.create(id='ID')
            self.assertEqual(
                context.exception.message, "'email' must be set")

    def test_requires_first_name(self):
        with self.assertRaises(ValueError) as context:
            self.component.create(id='ID', email='foo@bar.com')
            self.assertEqual(
                context.exception.message, "'first_name' must be set")

    def test_requires_last_name(self):
        with self.assertRaises(ValueError) as context:
            self.component.create(
                id='ID', email='foo@bar.com', first_name='foo')
            self.assertEqual(
                context.exception.message, "'last_name' must be set")


if __name__ == '__main__':
    unittest.main()
