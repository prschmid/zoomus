import datetime
import json
import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from zoomus import API_VERSION_1, util


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ApiClientTestCase))
    suite.addTest(unittest.makeSuite(RequireKeysTestCase))
    suite.addTest(unittest.makeSuite(DateToStrTestCase))
    suite.addTest(unittest.makeSuite(IsStrTypeTestCase))
    return suite


class ApiClientTestCase(unittest.TestCase):
    def test_init_sets_config(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        self.assertEqual(client.base_uri, "http://www.foo.com")
        self.assertEqual(client.timeout, 15)

    def test_init_sets_config_with_timeout(self):
        client = util.ApiClient(base_uri="http://www.foo.com", timeout=500)
        self.assertEqual(client.timeout, 500)

    def test_cannot_init_with_non_int_timeout(self):
        with self.assertRaises(ValueError) as context:
            util.ApiClient(base_uri="http://www.foo.com", timeout="bad")
            self.assertEqual(
                context.exception.message, "timeout value must be an integer"
            )

    def test_can_get_base_uri(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        self.assertEqual(client.base_uri, "http://www.foo.com")

    def test_can_set_base_uri(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        client.base_uri = "http://www.bar.com"
        self.assertEqual(client.base_uri, "http://www.bar.com")

    def test_set_base_uri_removes_trailing_slash(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        client.base_uri = "http://www.bar.com/"
        self.assertEqual(client.base_uri, "http://www.bar.com")

    def test_can_get_timeout(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        self.assertEqual(client.timeout, 15)

    def test_can_set_timeout(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        client.timeout = 500
        self.assertEqual(client.timeout, 500)

    def test_cannot_set_timeout_to_non_int(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        with self.assertRaises(ValueError) as context:
            client.timeout = "bad"
            self.assertEqual(
                context.exception.message, "timeout value must be an integer"
            )

    def test_url_for_returns_complete_url(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        self.assertEqual(client.url_for("bar"), "http://www.foo.com/bar")

    def test_url_for_ignores_preceding_slash(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        self.assertEqual(client.url_for("/bar"), "http://www.foo.com/bar")

    def test_url_for_ignores_trailing_slash(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        self.assertEqual(client.url_for("bar/"), "http://www.foo.com/bar")

    @patch("requests.get")
    def test_can_get_request(self, mocked_get):

        mocked_get.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.get_request("endpoint")

        mocked_get.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            headers=None,
            timeout=client.timeout,
        )

    @patch("requests.get")
    def test_can_get_request_with_params(self, mocked_get):

        mocked_get.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.get_request("endpoint", params={"foo": "bar"})

        mocked_get.assert_called_with(
            client.url_for("endpoint"),
            params={"foo": "bar"},
            headers=None,
            timeout=client.timeout,
        )

    @patch("requests.get")
    def test_can_get_request_with_headers(self, mocked_get):

        mocked_get.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.get_request("endpoint", headers={"foo": "bar"})

        mocked_get.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            headers={"foo": "bar"},
            timeout=client.timeout,
        )

    @patch("requests.post")
    def test_can_post_request(self, mocked_post):

        mocked_post.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.post_request("endpoint")

        mocked_post.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.post")
    def test_can_post_request_with_params(self, mocked_post):

        mocked_post.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.post_request("endpoint", params={"foo": "bar"})

        mocked_post.assert_called_with(
            client.url_for("endpoint"),
            params={"foo": "bar"},
            data=None,
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.post")
    def test_can_post_request_with_dict_data(self, mocked_post):

        mocked_post.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.post_request("endpoint", data={"foo": "bar"})

        mocked_post.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=json.dumps({"foo": "bar"}),
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.post")
    def test_can_post_request_with_json_data(self, mocked_post):

        mocked_post.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.post_request("endpoint", data=json.dumps({"foo": "bar"}))

        mocked_post.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=json.dumps({"foo": "bar"}),
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.post")
    def test_can_post_request_with_headers(self, mocked_post):

        mocked_post.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.post_request("endpoint", headers={"foo": "bar"})

        mocked_post.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers={"foo": "bar"},
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.post")
    def test_can_post_request_with_cookies(self, mocked_post):

        mocked_post.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.post_request("endpoint", cookies={"foo": "bar"})

        mocked_post.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers=None,
            cookies={"foo": "bar"},
            timeout=client.timeout,
        )

    @patch("requests.patch")
    def test_can_patch_request(self, mocked_patch):

        mocked_patch.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.patch_request("endpoint")

        mocked_patch.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.patch")
    def test_can_patch_request_with_params(self, mocked_patch):

        mocked_patch.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.patch_request("endpoint", params={"foo": "bar"})

        mocked_patch.assert_called_with(
            client.url_for("endpoint"),
            params={"foo": "bar"},
            data=None,
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.patch")
    def test_can_patch_request_with_dict_data(self, mocked_patch):

        mocked_patch.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.patch_request("endpoint", data={"foo": "bar"})

        mocked_patch.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=json.dumps({"foo": "bar"}),
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.patch")
    def test_can_patch_request_with_json_data(self, mocked_patch):

        mocked_patch.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.patch_request("endpoint", data=json.dumps({"foo": "bar"}))

        mocked_patch.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=json.dumps({"foo": "bar"}),
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.patch")
    def test_can_patch_request_with_headers(self, mocked_patch):

        mocked_patch.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.patch_request("endpoint", headers={"foo": "bar"})

        mocked_patch.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers={"foo": "bar"},
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.patch")
    def test_can_patch_request_with_cookies(self, mocked_patch):

        mocked_patch.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.patch_request("endpoint", cookies={"foo": "bar"})

        mocked_patch.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers=None,
            cookies={"foo": "bar"},
            timeout=client.timeout,
        )

    @patch("requests.delete")
    def test_can_delete_request(self, mocked_delete):

        mocked_delete.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.delete_request("endpoint")

        mocked_delete.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.delete")
    def test_can_delete_request_with_params(self, mocked_delete):

        mocked_delete.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.delete_request("endpoint", params={"foo": "bar"})

        mocked_delete.assert_called_with(
            client.url_for("endpoint"),
            params={"foo": "bar"},
            data=None,
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.delete")
    def test_can_delete_request_with_dict_data(self, mocked_delete):

        mocked_delete.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.delete_request("endpoint", data={"foo": "bar"})

        mocked_delete.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=json.dumps({"foo": "bar"}),
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.delete")
    def test_can_delete_request_with_json_data(self, mocked_delete):

        mocked_delete.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.delete_request("endpoint", data=json.dumps({"foo": "bar"}))

        mocked_delete.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=json.dumps({"foo": "bar"}),
            headers=None,
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.delete")
    def test_can_delete_request_with_headers(self, mocked_delete):

        mocked_delete.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.delete_request("endpoint", headers={"foo": "bar"})

        mocked_delete.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers={"foo": "bar"},
            cookies=None,
            timeout=client.timeout,
        )

    @patch("requests.delete")
    def test_can_delete_request_with_cookies(self, mocked_delete):

        mocked_delete.side_effect = lambda *args, **kwargs: True

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": API_VERSION_1}
        )
        client.delete_request("endpoint", cookies={"foo": "bar"})

        mocked_delete.assert_called_with(
            client.url_for("endpoint"),
            params=None,
            data=None,
            headers=None,
            cookies={"foo": "bar"},
            timeout=client.timeout,
        )


class RequireKeysTestCase(unittest.TestCase):
    def test_can_require_keys_with_single_string_key(self):
        d = {"a": 1}
        with self.assertRaises(ValueError) as context:
            util.require_keys(d, "b")
            self.assertEqual(context.exception.message, "'b' must be set")

    def test_can_require_keys_with_list_keys(self):
        d = {"a": 1}
        with self.assertRaises(ValueError) as context:
            util.require_keys(d, ["b"])
            self.assertEqual(context.exception.message, "'b' must be set")

    def test_can_require_keys_with_multi_item_list_keys(self):
        d = {"a": 1, "b": 2}
        with self.assertRaises(ValueError) as context:
            util.require_keys(d, ["b", "c"])
            self.assertEqual(context.exception.message, "'c' must be set")

    def test_require_keys_with_dict_raises_error_if_missing(self):
        d = {"a": 1}
        with self.assertRaises(ValueError) as context:
            util.require_keys(d, "b")
            self.assertEqual(context.exception.message, "'b' must be set")

    def test_require_keys_with_dict_does_not_raises_error_if_none_by_default(self):
        d = {"a": 1, "b": None}
        self.assertTrue(util.require_keys(d, "b"))

    def test_require_keys_with_dict_does_raises_error_if_none_not_allowed(self):
        d = {"a": 1, "b": None}
        with self.assertRaises(ValueError) as context:
            self.assertTrue(util.require_keys(d, "b", allow_none=False))
            self.assertEqual(context.exception.message, "'b' cannot be None")


class DateToStrTestCase(unittest.TestCase):
    def test_can_convert_date_to_str(self):
        d = datetime.date(year=2015, month=12, day=8)
        self.assertEqual(util.date_to_str(d), "2015-12-08T00:00:00Z")

    def test_can_convert_datetime_to_str(self):
        d = datetime.datetime(year=2015, month=12, day=8, hour=23, minute=21, second=37)
        self.assertEqual(util.date_to_str(d), "2015-12-08T23:21:37Z")


class IsStrTypeTestCase(unittest.TestCase):

    from sys import version_info

    def test_str_is_str_type(self):
        self.assertTrue(util.is_str_type("s"))

    def test_numeric_str_is_str_type(self):
        self.assertTrue(util.is_str_type("5"))

    def test_non_str_is_not_str_type(self):
        self.assertFalse(util.is_str_type(5))

    @unittest.skipIf(version_info[0] >= 3, "No applicable to Python 3+")
    def test_unicode_is_str_type(self):
        self.assertTrue(util.is_str_type(unicode("s")))

    @unittest.skipIf(version_info[0] >= 3, "No applicable to Python 3+")
    def test_numeric_unicode_is_str_type(self):
        self.assertTrue(util.is_str_type(unicode("5")))


if __name__ == "__main__":
    unittest.main()
