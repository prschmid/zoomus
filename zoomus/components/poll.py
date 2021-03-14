"""Zoom.us REST API Python Client -- Recording component"""
from zoomus import util
from zoomus.components import base


class PollComponentV2(base.BaseComponent):
    def __init__(self, *args, **kwargs):
        util.require_keys(kwargs, "type")
        self.type = kwargs.get('type')
        super().__init__(*args, **kwargs)

    def list(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request(
            "/{}/{}/polls".format(
                self.type, kwargs.get("id")
            )
        )

    def create(self, **kwargs):
        util.require_keys(kwargs, "id")
        util.require_keys(kwargs, "data")
        return self.post_request(
            "/{}/{}/polls".format(
                self.type, kwargs.get('id')
            ),
            data=kwargs.get('data')
        )

    def get(self, **kwargs):
        util.require_keys(kwargs, "id")
        util.require_keys(kwargs, "poll_id")
        return self.get_request(
            "/{}/{kwargs.get('id')}/polls/{}".format(
                self.type, kwargs.get('poll_id')
            )
        )

    def update(self, **kwargs):
        util.require_keys(kwargs, "id")
        util.require_keys(kwargs, "poll_id")
        util.require_keys(kwargs, "data")
        return self.patch_request(
            "/{}/{kwargs.get('id')}/polls/{}".format(
                self.type, kwargs.get('poll_id')
            ),
            data=kwargs.get('data')
        )

    def delete(self, **kwargs):
        util.require_keys(kwargs, "id")
        util.require_keys(kwargs, "poll_id")
        return self.delete_request(
            "/{}/{kwargs.get('id')}/polls/{}".format(
                self.type, kwargs.get('poll_id')
            )
        )

    class Meta:
        abstract = True


class WebinarPollComponentV2(PollComponentV2):
    def __init__(self, *args, **kwargs):
        kwargs['type'] = 'webinars'
        super().__init__(*args, **kwargs)


class MeetingsPollComponentV2(PollComponentV2):
    def __init__(self, *args, **kwargs):
        kwargs['type'] = 'meetings'
        super().__init__(*args, **kwargs)
