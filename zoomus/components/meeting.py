"""Zoom.us REST API Python Client"""

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

from zoomus import util
from zoomus.components import base


class MeetingComponent(base.BaseComponent):
    """Component dealing with all meeting related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, 'host_id')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request("/meeting/list", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, ['host_id', 'topic', 'type'])
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request("/meeting/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request("/meeting/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        return self.post_request("/meeting/delete", params=kwargs)

    def end(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        return self.post_request("/meeting/end", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, ['id', 'host_id'])
        return self.post_request("/meeting/get", params=kwargs)