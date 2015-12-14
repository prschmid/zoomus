__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

import unittest

from mock import patch

from zoomus import (
    components,
    util)


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseComponentTestCase))
    return suite


class BaseComponentTestCase(unittest.TestCase):

    def test_post_request_includes_config_details_in_data_when_no_data(self):

        with patch.object(util.ApiClient, 'post_request',
                          return_value=True) as mock_post_request:

            component = components.base.BaseComponent(
                base_uri="http://www.foo.com",
                config={'api_key': 'KEY', 'api_secret': 'SECRET'})
            component.post_request("foo")
            mock_post_request.assert_called_with(
                "foo",
                params=component.config,
                data=None,
                headers=None,
                cookies=None
            )

    def test_post_request_includes_config_details_in_data_when_there_is_data(self):

        with patch.object(util.ApiClient, 'post_request',
                          return_value=True) as mock_post_request:

            component = components.base.BaseComponent(
                base_uri="http://www.foo.com",
                config={'api_key': 'KEY', 'api_secret': 'SECRET'})
            component.post_request("foo", params={'foo': 'bar'})

            params = {'foo': 'bar'}
            params.update(component.config)

            mock_post_request.assert_called_with(
                "foo",
                params=params,
                data=None,
                headers=None,
                cookies=None
            )


if __name__ == '__main__':
    unittest.main()
