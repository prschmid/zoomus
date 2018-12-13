"""Zoom.us REST API Python Client"""

from __future__ import absolute_import

from zoomus import (
    components,
    util)


class ZoomClient(util.ApiClient):
    """Zoom.us REST API Python Client"""

    BASE_URI_V1 = 'https://api.zoom.us/v1'
    BASE_URI_V2 = 'https://api.zoom.us/v2'
    """Base URL for Zoom API"""

    def __init__(
            self, api_key, api_secret, data_type='json', timeout=15, version=1):
        """Create a new Zoom client

        :param api_key: The Zooom.us API key
        :param api_secret: The Zoom.us API secret
        :param data_type: The expected return data type. Either 'json' or 'xml'
        :param timeout: The time out to use for API requets
        """
        BASE_URI = ZoomClient.BASE_URI_V1 if version == 1 else ZoomClient.BASE_URI_V2

        super(ZoomClient, self).__init__(
            base_uri=BASE_URI, timeout=timeout)

        # Setup the config details
        self.config = {
            'api_key': api_key,
            'api_secret': api_secret,
            'data_type': data_type,
            'version': version,
            'token': util.generate_jwt(api_key, api_secret),
        }

        class_user_component = components.user.UserComponent if version == 1 else components.user.UserComponentV2
        class_meeting_component = components.meeting.MeetingComponent if version == 1 else components.meeting.MeetingComponentV2
        class_recording_component = components.recording.RecordingComponent if version == 1 else components.recording.RecordingComponentV2
        class_webinar_component = components.webinar.WebinarComponent if version == 1 else components.webinar.WebinarComponentV2
        class_report_component = components.report.ReportComponent if version == 1 else components.report.ReportComponentV2

        # Register all of the components
        self.components = {
            'meeting': class_meeting_component(
                base_uri=BASE_URI, config=self.config),
            'report': class_report_component(
                base_uri=BASE_URI, config=self.config),
            'user': class_user_component(
                base_uri=BASE_URI, config=self.config),
            'webinar': class_webinar_component(
                base_uri=BASE_URI, config=self.config),
            'recording': class_recording_component(
                base_uri=BASE_URI, config=self.config)
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def refresh_token(self):
        self.config['token'] = util.generate_jwt(
            self.config['api_key'],
            self.config['api_secret']),

    @property
    def api_key(self):
        """The Zoom.us api_key"""
        return self.config.get('api_key')

    @api_key.setter
    def api_key(self, value):
        """Set the api_key"""
        self.config['api_key'] = value
        self.refresh_token()

    @property
    def api_secret(self):
        """The Zoom.us api_secret"""
        return self.config.get('api_secret')

    @api_secret.setter
    def api_secret(self, value):
        """Set the api_secret"""
        self.config['api_secret'] = value
        self.refresh_token()

    @property
    def meeting(self):
        """Get the meeting component"""
        return self.components.get('meeting')

    @property
    def report(self):
        """Get the report component"""
        return self.components.get('report')

    @property
    def user(self):
        """Get the user component"""
        return self.components.get('user')

    @property
    def webinar(self):
        """Get the webinar component"""
        return self.components.get('webinar')

    @property
    def recording(self):
        """Get the recording component"""
        return self.components.get('recording')
