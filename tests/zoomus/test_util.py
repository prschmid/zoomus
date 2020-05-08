import datetime
import json
import unittest

from zoomus import util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ApiClientTestCase))
    suite.addTest(unittest.makeSuite(RequireKeysTestCase))
    suite.addTest(unittest.makeSuite(DateToStrTestCase))
    suite.addTest(unittest.makeSuite(IsStrTypeTestCase))
    suite.addTest(unittest.makeSuite(EncodeUuidTestCase))
    return suite


class ApiClientTestCase(unittest.TestCase):
    def test_init_sets_config(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        self.assertEqual(client.base_uri, "http://www.foo.com")
        self.assertEqual(client.timeout, 15)

    def test_init_sets_config_with_timeout(self):
        client = util.ApiClient(base_uri="http://www.foo.com", timeout=500)
        self.assertEqual(client.timeout, 500)

    def test_init_sets_config_with_timeout_none(self):
        client = util.ApiClient(base_uri="http://www.foo.com", timeout=None)
        self.assertEqual(client.timeout, None)

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

    def test_can_set_timeout(self):
        client = util.ApiClient(base_uri="http://www.foo.com")
        client.timeout = None
        self.assertEqual(client.timeout, None)

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

    @responses.activate
    def test_can_multiple_request_with_session(self):
        responses.add(responses.GET, "http://www.foo.com/endpoint")
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.get_request("endpoint")
            client.post_request("endpoint")
            client.patch_request("endpoint")
            client.delete_request("endpoint")

    @responses.activate
    def test_can_get_request(self):
        responses.add(responses.GET, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.get_request("endpoint")

    @responses.activate
    def test_can_get_request_with_session(self):
        responses.add(responses.GET, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.get_request("endpoint")

    @responses.activate
    def test_can_get_request_v2(self):
        responses.add(
            responses.GET, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.get_request("endpoint")
        expected_headers = {"Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_get_request_with_params(self):
        responses.add(responses.GET, "http://www.foo.com/endpoint?foo=bar")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.get_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_get_request_with_params_and_session(self):
        responses.add(responses.GET, "http://www.foo.com/endpoint?foo=bar")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.get_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_get_request_with_params_v2(self):
        responses.add(
            responses.GET, "http://www.foo.com/endpoint?foo=bar",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.get_request("endpoint", params={"foo": "bar"})
        expected_headers = {"Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_get_request_with_headers(self):
        responses.add(
            responses.GET, "http://www.foo.com/endpoint", headers={"foo": "bar"}
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.get_request("endpoint", headers={"foo": "bar"})

    @responses.activate
    def test_can_get_request_with_headers_and_session(self):
        responses.add(
            responses.GET, "http://www.foo.com/endpoint", headers={"foo": "bar"}
        )
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.get_request("endpoint", headers={"foo": "bar"})

    @responses.activate
    def test_can_get_request_with_headers_v2(self):
        responses.add(
            responses.GET, "http://www.foo.com/endpoint", headers={"foo": "bar"}
        )

        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.get_request("endpoint", headers={"foo": "bar"})

    @responses.activate
    def test_can_post_request(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")

        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.post_request("endpoint")

    @responses.activate
    def test_can_post_request(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")

        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.post_request("endpoint")

    @responses.activate
    def test_can_post_request_v2(self):
        responses.add(
            responses.POST, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.post_request("endpoint")
        expected_headers = {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_post_request_with_params(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint?foo=bar")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.post_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_post_request_with_params_and_session(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint?foo=bar")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.post_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_post_request_with_params_v2(self):
        responses.add(
            responses.POST, "http://www.foo.com/endpoint?foo=bar",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.post_request("endpoint", params={"foo": "bar"})
        expected_headers = {"Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_post_request_with_dict_data(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.post_request("endpoint", data={"foo": "bar"})
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_post_request_with_dict_data_and_session(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.post_request("endpoint", data={"foo": "bar"})
            self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_post_request_with_dict_data_v2(self):
        responses.add(
            responses.POST, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.post_request("endpoint", data={"foo": "bar"})
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')
        expected_headers = {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_post_request_with_json_data(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.post_request("endpoint", data=json.dumps({"foo": "bar"}))
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_post_request_with_json_data_and_session(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.post_request("endpoint", data=json.dumps({"foo": "bar"}))
            self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_post_request_with_json_data_v2(self):
        responses.add(
            responses.POST, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.post_request("endpoint", data=json.dumps({"foo": "bar"}))
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')
        expected_headers = {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_post_request_with_headers(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.post_request("endpoint", headers={"foo": "bar"})
        expected_headers = {"foo": "bar"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_post_request_with_headers_and_session(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.post_request("endpoint", headers={"foo": "bar"})
            expected_headers = {"foo": "bar"}
            actual_headers = responses.calls[0].request.headers
            self.assertTrue(
                set(expected_headers.items()).issubset(set(actual_headers.items()))
            )

    @responses.activate
    def test_can_post_request_with_headers_v2(self):
        responses.add(
            responses.POST, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.post_request("endpoint", headers={"foo": "bar"})
        expected_headers = {"foo": "bar"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_post_request_with_cookies(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.post_request("endpoint", cookies={"foo": "bar"})
        expected_headers = {"Cookie": "foo=bar"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_post_request_with_cookies_and_session(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.post_request("endpoint", cookies={"foo": "bar"})
            expected_headers = {"Cookie": "foo=bar"}
            actual_headers = responses.calls[0].request.headers
            self.assertTrue(
                set(expected_headers.items()).issubset(set(actual_headers.items()))
            )

    @responses.activate
    def test_can_post_request_with_cookies_v2(self):
        responses.add(responses.POST, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.post_request("endpoint", cookies={"foo": "bar"})
        expected_headers = {"Cookie": "foo=bar", "Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.patch_request("endpoint")

    @responses.activate
    def test_can_patch_request_with_session(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.patch_request("endpoint")

    @responses.activate
    def test_can_patch_request_v2(self):
        responses.add(
            responses.PATCH, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.patch_request("endpoint")
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request_with_params(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint?foo=bar")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.patch_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_patch_request_with_params_and_session(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint?foo=bar")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.patch_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_patch_request_with_params_v2(self):
        responses.add(
            responses.PATCH, "http://www.foo.com/endpoint?foo=bar",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.patch_request("endpoint", params={"foo": "bar"})
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request_with_dict_data(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.patch_request("endpoint", data={"foo": "bar"})
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_patch_request_with_dict_data_and_session(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.patch_request("endpoint", data={"foo": "bar"})
            self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_patch_request_with_dict_data_v2(self):
        responses.add(
            responses.PATCH, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.patch_request("endpoint", data={"foo": "bar"})
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request_with_json_data(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.patch_request("endpoint", data=json.dumps({"foo": "bar"}))
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_patch_request_with_json_data_and_session(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.patch_request("endpoint", data=json.dumps({"foo": "bar"}))
            self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_patch_request_with_json_data_v2(self):
        responses.add(
            responses.PATCH, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.patch_request("endpoint", data=json.dumps({"foo": "bar"}))
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request_with_headers(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.patch_request("endpoint", headers={"foo": "bar"})
        expected_headers = {"foo": "bar"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request_with_headers_and_session(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.patch_request("endpoint", headers={"foo": "bar"})
            expected_headers = {"foo": "bar"}
            actual_headers = responses.calls[0].request.headers
            self.assertTrue(
                set(expected_headers.items()).issubset(set(actual_headers.items()))
            )

    @responses.activate
    def test_can_patch_request_with_headers_v2(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.patch_request("endpoint", headers={"foo": "bar"})
        expected_headers = {"foo": "bar"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request_with_cookies(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.patch_request("endpoint", cookies={"foo": "bar"})
        expected_headers = {"Cookie": "foo=bar"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_patch_request_with_cookies_and_session(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.patch_request("endpoint", cookies={"foo": "bar"})
            expected_headers = {"Cookie": "foo=bar"}
            actual_headers = responses.calls[0].request.headers
            self.assertTrue(
                set(expected_headers.items()).issubset(set(actual_headers.items()))
            )

    @responses.activate
    def test_can_patch_request_with_cookies_v2(self):
        responses.add(responses.PATCH, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.patch_request("endpoint", cookies={"foo": "bar"})
        expected_headers = {"Cookie": "foo=bar", "Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_delete_request(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.delete_request("endpoint")

    @responses.activate
    def test_can_delete_request_with_session(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.delete_request("endpoint")

    @responses.activate
    def test_can_delete_request_v2(self):
        responses.add(
            responses.DELETE, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.delete_request("endpoint")
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_delete_request_with_params(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint?foo=bar")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )

        client.delete_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_delete_request_with_params_and_session(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint?foo=bar")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.delete_request("endpoint", params={"foo": "bar"})

    @responses.activate
    def test_can_delete_request_with_params_v2(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint?foo=bar")
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.delete_request("endpoint", params={"foo": "bar"})
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_delete_request_with_dict_data(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.delete_request("endpoint", data={"foo": "bar"})
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_delete_request_with_dict_data_and_session(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.delete_request("endpoint", data={"foo": "bar"})
            self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_delete_request_with_dict_data_v2(self):
        responses.add(
            responses.DELETE, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.delete_request("endpoint", data={"foo": "bar"})
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_delete_request_with_json_data(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.delete_request("endpoint", data=json.dumps({"foo": "bar"}))
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_delete_request_with_json_data_and_session(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.delete_request("endpoint", data=json.dumps({"foo": "bar"}))
            self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')

    @responses.activate
    def test_can_delete_request_with_json_data_v2(self):
        responses.add(
            responses.DELETE, "http://www.foo.com/endpoint",
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.delete_request("endpoint", data=json.dumps({"foo": "bar"}))
        self.assertEqual(responses.calls[0].request.body, '{"foo": "bar"}')
        expected_headers = {
            "Authorization": "Bearer token",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_delete_request_with_headers(self):
        responses.add(
            responses.DELETE, "http://www.foo.com/endpoint", headers={"foo": "bar"}
        )
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.delete_request("endpoint", headers={"foo": "bar"})

    @responses.activate
    def test_can_delete_request_with_headers_and_session(self):
        responses.add(
            responses.DELETE, "http://www.foo.com/endpoint", headers={"foo": "bar"}
        )
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.delete_request("endpoint", headers={"foo": "bar"})

    @responses.activate
    def test_can_delete_request_with_headers_v2(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.delete_request("endpoint", headers={"foo": "bar"})
        expected_headers = {
            "foo": "bar",
        }
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_delete_request_with_cookies(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        )
        client.delete_request("endpoint", cookies={"foo": "bar"})
        expected_headers = {"Cookie": "foo=bar"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
        )

    @responses.activate
    def test_can_delete_request_with_cookies_and_session(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        with util.ApiClient(
            base_uri="http://www.foo.com", config={"version": util.API_VERSION_1}
        ) as client:
            client.delete_request("endpoint", cookies={"foo": "bar"})
            expected_headers = {"Cookie": "foo=bar"}
            actual_headers = responses.calls[0].request.headers
            self.assertTrue(
                set(expected_headers.items()).issubset(set(actual_headers.items()))
            )

    @responses.activate
    def test_can_delete_request_with_cookies_v2(self):
        responses.add(responses.DELETE, "http://www.foo.com/endpoint")
        client = util.ApiClient(
            base_uri="http://www.foo.com",
            config={"version": util.API_VERSION_2, "token": "token"},
        )
        client.delete_request("endpoint", cookies={"foo": "bar"})
        expected_headers = {"Cookie": "foo=bar", "Authorization": "Bearer token"}
        actual_headers = responses.calls[0].request.headers
        self.assertTrue(
            set(expected_headers.items()).issubset(set(actual_headers.items()))
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


class EncodeUuidTestCase(unittest.TestCase):
    def test_encode_without_slash(self):
        uuid = "i6fJBQh0QzWCgrKretYGjg=="
        self.assertEqual(util.encode_uuid(uuid), "i6fJBQh0QzWCgrKretYGjg==")

    def test_encode_with_leading_slash(self):
        uuid = "/6fJBQh0QzWCgrKretYGjg=="
        self.assertEqual(util.encode_uuid(uuid), "%252F6fJBQh0QzWCgrKretYGjg%253D%253D")

    def test_encode_with_double_slash(self):
        uuid = "i6fJBQh0Qz//grKretYGjg=="
        self.assertEqual(
            util.encode_uuid(uuid), "i6fJBQh0Qz%252F%252FgrKretYGjg%253D%253D"
        )


if __name__ == "__main__":
    unittest.main()
