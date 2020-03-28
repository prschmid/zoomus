"""Zoom.us REST API Python Client -- Webinar component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class WebinarComponent(base.BaseComponent):
    """Component dealing with all webinar related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, "host_id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/webinar/list", params=kwargs)

    def upcoming(self, **kwargs):
        util.require_keys(kwargs, "host_id")
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/webinar/list/registration", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, ["host_id", "topic"])
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/webinar/create", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/webinar/update", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/webinar/delete", params=kwargs)

    def end(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/webinar/end", params=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, ["id", "host_id"])
        return self.post_request("/webinar/get", params=kwargs)

    def register(self, **kwargs):
        util.require_keys(kwargs, ["id", "email", "first_name", "last_name"])
        if kwargs.get("start_time"):
            kwargs["start_time"] = util.date_to_str(kwargs["start_time"])
        return self.post_request("/webinar/register", params=kwargs)


class WebinarComponentV2(base.BaseComponent):
    """Component dealing with all webinar related matters"""
    API_ENDPOINTS = {
        "WEBINAR_LIST": "/users/{}/webinars",
        "WEBINAR_CREATE": "/users/{}/webinars",
        "WEBINAR_UPDATE": "/webinars/{}",
        "WEBINAR_DELETE": "/webinars/{}",
        "WEBINAR_END": "/webinars/{}/status",
        "WEBINAR_DETAIL": "/webinars/{}",
        "WEBINAR_ATTENDEE_REGISTER": "/webinars/{}/registrants",
        "WEBINAR_ATTENDEE_LIST": "/webinars/{}/registrants",
        "WEBINAR_ATTENDEE_DETAIL": "/webinars/{}/registrants/{}",
        "WEBINAR_ATTENDEE_STATUS": "/webinars/{}/registrants/status",
    }

    def list(self, user_id, **kwargs):
        """
        Method to list My Webinars for given user ID.
        :param user_id: User ID (Host ID)
        :param kwargs: query params
        :return: Response Object
        """
        return self.get_request(
            self.API_ENDPOINTS["WEBINAR_LIST"].format(user_id), params=kwargs
        )

    def create(self, user_id, payload=None, **kwargs):
        """
        Method to create a Webinar.
        :param user_id: User ID (Host ID)
        :param payload: Dict containing Webinar details & settings
        :param kwargs: query params
        :return: Response Object
        """
        return self.post_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_CREATE"].format(user_id),
            params=kwargs,
            data=payload
        )

    def update(self, webinar_id, payload=None, **kwargs):
        """
        Method to update an Existing Webinar.
        :param webinar_id: Webinar ID
        :param payload: Dict containing Webinar details & settings to be updated
        :param kwargs: Query params
        :return: Response Object
        """
        return self.patch_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_UPDATE"].format(webinar_id),
            params=kwargs,
            data=payload
        )

    def delete(self, webinar_id, **kwargs):
        """
        Method to delete a Webinar
        :param webinar_id: Webinar ID
        :param kwargs: Query params
        :return: Response Object
        """
        return self.delete_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_DELETE"].format(webinar_id),
            params=kwargs
        )

    def end(self, webinar_id, **kwargs):
        """
        Method to update Webinar status as ended.
        :param webinar_id: Webinar ID to be ended
        :param kwargs: Query params
        :return: Response Object
        """
        return self.put_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_END"].format(webinar_id),
            params=kwargs,
            data={"status": "end"}
        )

    def get(self, webinar_id, **kwargs):
        """
        Method to fetch Webinar Details & Its Setting.
        :param webinar_id: Webinar ID whose detail is to be fetched.
        :param kwargs: Query params
        :return: Response Object
        """
        return self.get_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_DETAIL"].format(webinar_id),
            params=kwargs
        )

    def register(self, webinar_id, payload=None, **kwargs):
        """
        Method to add Attendee in a Webinar.
        :param webinar_id: Webinar ID in which attendee needs to be added.
        :param payload: Dict containing Attendee Details
        :param kwargs: Query params
        :return: Response Object
        """
        util.require_keys(payload, ["email", "first_name", "last_name"])
        return self.post_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_ATTENDEE_REGISTER"].format(webinar_id),
            params=kwargs,
            data=payload
        )

    def get_registrant(self, webinar_id, registrant_id, **kwargs):
        """
        Method to fetch a Registrant/Attendee Details.
        :param webinar_id: Webinar ID
        :param registrant_id: Registrant ID
        :param kwargs: Query params
        :return: Response Object
        """
        return self.get_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_ATTENDEE_DETAIL"].format(webinar_id, registrant_id),
            params=kwargs,
        )

    def update_registrants_status(self, webinar_id, payload=None, **kwargs):
        """
        Method to update Registrant/Attendee Status to Approved, Deny or Cancel.
        :param webinar_id: Webinar ID
        :param payload: Dict containing action.
        :param kwargs: Query params
        :return: Response Object
        """
        return self.put_request(
            endpoint=self.API_ENDPOINTS["WEBINAR_ATTENDEE_STATUS"].format(webinar_id),
            params=kwargs,
            data=payload
        )
