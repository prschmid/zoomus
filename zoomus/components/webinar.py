"""Zoom.us REST API Python Client -- Webinar component"""

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

from zoomus import util
from zoomus.components import base


class WebinarComponent(base.BaseComponent):
    """Component dealing with all webinar related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, 'host_id')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request("/webinar/list", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, ['host_id', 'topic'])
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request("/webinar/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request("/webinar/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        return self.post_request("/webinar/delete", params=kwargs)

    def end(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        return self.post_request("/webinar/end", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        return self.post_request("/webinar/get", params=kwargs)

    def register(self, **kwargs):
        util.require_keys(kwargs, ['id', 'email', 'first_name', 'last_name'])
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request("/webinar/register", params=kwargs)