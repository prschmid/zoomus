"""Zoom.us REST API Python Client -- Phone component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class PhoneComponentV2(base.BaseComponent):
    def numbers_list(self, **kwargs):
        return self.get_request("/phone/numbers", params=kwargs)

    def numbers_get(self, **kwargs):
        util.require_keys(kwargs, "id")
        return self.get_request(
            "/phone/numbers/{}".format(kwargs.get("id")), params=kwargs
        )

    def call_logs(self, **kwargs):
        """
        Retrieve call logs for an account.

        Scopes: phone:read:admin

        Prerequisite:
        * Business or Enterprise account
        * A Zoom Phone license
        * Account Owner and a  with Zoom Phone Management

        :param page_size: The number of records returned within a single API call,
        default=30, max=300
        :param page_number: The current page number of returned records, default=1
        :param from: Start date from which you would like to get the call logs. The start date should be within past six months.
        :param to: The end date upto which you would like to get the call logs for.
        The end date should be within past six months.
        :param type: The type of the call logs. The value can be either "all" or "missed".
        :return: request object with json data
        """
        return self.get_request("/phone/call_logs", params=kwargs)

    def calling_plans(self, **kwargs):
        return self.get_request("/phone/calling_plans", params=kwargs)

    def users(self, **kwargs):
        return self.get_request("/phone/users", params=kwargs)
