"""Zoom.us REST API Python Client -- User component"""

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

from zoomus import util
from zoomus.components import base


class UserComponent(base.BaseComponent):
    """Component dealing with all user related matters"""

    def list(self, **kwargs):
        return self.post_request("/user/list", params=kwargs)

    def pending(self, **kwargs):
        return self.post_request("/user/pending", params=kwargs)

    def create(self, **kwargs):
        return self.post_request("/user/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, 'id')
        return self.post_request("/user/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, 'id')
        return self.post_request("/user/delete", params=kwargs)

    def cust_create(self, **kwargs):
        util.require_keys(kwargs, ['type', 'email'])
        return self.post_request("/user/custcreate", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, 'id')
        return self.post_request("/user/get", params=kwargs)

    def get_by_email(self, **kwargs):
        util.require_keys(kwargs, ['email', 'login_type'])
        return self.post_request("/user/getbyemail", params=kwargs)
