"""Zoom.us REST API Python Client -- User component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class UserComponent(base.BaseComponent):
    """Component dealing with all user related matters"""

    def me(self):
        return self.get_request("/user/me")

    def list(self, **kwargs):
        return self.post_request("/user/list", params=kwargs)

    def pending(self, **kwargs):
        return self.post_request("/user/pending", params=kwargs)

    def create(self, **kwargs):
        return self.post_request("/user/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.post_request("/user/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.post_request("/user/delete", params=kwargs)

    def cust_create(self, **kwargs):
        util.require_keys(kwargs, ["type", "email"])
        return self.post_request("/user/custcreate", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.post_request("/user/get", params=kwargs)

    def get_by_email(self, **kwargs):
        util.require_keys(kwargs, ["email", "login_type"])
        return self.post_request("/user/getbyemail", params=kwargs)


class UserComponentV2(base.BaseComponent):
    def me(self):
        return self.get_request("/users/me")

    def list(self, **kwargs):
        return self.get_request("/users", params=kwargs)

    def create(self, **kwargs):
        return self.post_request("/users", data=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.patch_request("/users/{}".format(kwargs.get("id")), data=kwargs)

    def update_settings(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.patch_request(
            "/users/{}/settings".format(kwargs.pop("id")), data=kwargs
        )

    def update_status(self, **kwargs):
        util.require_keys(kwargs, ["id", "action"])
        return self.put_request(
            "/users/{}/status".format(kwargs.pop("id")), data=kwargs
        )

    def check_email(self, **kwargs):
        """
        Verify if a user’s email is registered with Zoom.
        Expects:
            - email: string (Email address)
        Example:
            /users/email?email=foo@baar.test
        """
        util.require_keys(kwargs, "email")
        return self.get_request("/users/email", params=kwargs)

    def update_email(self, **kwargs):
        """
        Change a user’s  on a Zoom account that has managed domain set up.
        If the Zoom Account in which the user belongs, has multiple , the email to be updated must match one of the managed domains.

        Official docs: https://marketplace.zoom.us/docs/api-reference/zoom-api/users/useremailupdate

        Expects:
            - id: string (User ID)
            - email: string (New email address)

        Example:
            /users/42/email

            json:
                {"email": "foo@bar.new"}
        """
        util.require_keys(kwargs, "id")
        return self.put_request("/users/{}/email".format(kwargs.get("id")), data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.delete_request("/users/{}".format(kwargs.get("id")), params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request("/users/{}".format(kwargs.get("id")), params=kwargs)

    def get_settings(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request(
            "/users/{}/settings".format(kwargs.pop("id")), params=kwargs
        )
