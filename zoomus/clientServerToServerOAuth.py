import zoomus
import base64
import requests


# The currently availible library for Zoom still uses JWT. We will extend it
# and override a few things to get it working with Server-to-Server OAuth.
# Fortunatly, it all comes down to bearer tokens in the end, so we just need
# to patch a few things.
class ZoomClientServerToServerOAuth(zoomus.util.ApiClient):
    def __init__(
        self,
        account_id,
        client_id,
        client_secret,
        data_type="json",
        timeout=15,
        version=zoomus.util.API_VERSION_2,
    ):
        """Create a new Zoom client

        :param account_id: The Zooom.us API key
        :param client_id: The Zoom.us API secret
        :param client_secret: The Zoom.us API secret
        :param data_type: The expected return data type. Either 'json' or 'xml'
        :param timeout: The time out to use for API requests
        """
        try:
            BASE_URI = zoomus.client.API_BASE_URIS[version]
            self.components = zoomus.client.COMPONENT_CLASSES[version].copy()
        except KeyError:
            raise RuntimeError("API version not supported: %s" % version)

        super(ZoomClientServerToServerOAuth, self).__init__(
            base_uri=BASE_URI, timeout=timeout
        )

        auth_token = self.generate_s2sOAuthToken(
            account_id,
            client_id,
            client_secret
        )

        # Setup the config details
        self.config = {
            "account_id": account_id,
            "client_id": client_id,
            "client_secret": client_secret,
            "data_type": data_type,
            "version": version,
            "token": auth_token,
        }

        # Instantiate the components
        for key in self.components.keys():
            self.components[key] = self.components[key](
                base_uri=BASE_URI, config=self.config
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def generate_s2sOAuthToken(self, account_id, client_id, client_secret):
        base64_auth_string = base64.b64encode(
            f"{client_id}:{client_secret}".encode("ascii")
        ).decode("ascii")

        # Define the endpoint and payload
        url = "https://zoom.us/oauth/token"
        payload = {
            "grant_type": "account_credentials",
            "account_id": account_id,
        }

        # Define the headers
        headers = {
            "Authorization": f"Basic {base64_auth_string}",
        }

        # Make the request
        response = requests.post(url, data=payload, headers=headers)
        token = response.json().get("access_token")
        return token

    def refresh_token(self):
        self.config["token"] = (
            self.generate_s2sOAuthToken(
                self.config["account_id"],
                self.config["client_id"],
                self.config["client_secret"],
            ),
        )

    @property
    def client_secret(self):
        """The Zoom.us client_secret"""
        return self.config.get("client_secret")

    @client_secret.setter
    def client_secret(self, value):
        """Set the client_secret"""
        self.config["client_secret"] = value
        self.refresh_token()

    @property
    def account_id(self):
        """The Zoom.us account_id"""
        return self.config.get("account_id")

    @account_id.setter
    def account_id(self, value):
        """Set the account_id"""
        self.config["account_id"] = value
        self.refresh_token()

    @property
    def client_id(self):
        """The Zoom.us client_id"""
        return self.config.get("client_id")

    @client_id.setter
    def client_id(self, value):
        """Set the client_id"""
        self.config["client_id"] = value
        self.refresh_token()

    @property
    def contacts(self):
        """Get the contacts component"""
        return self.components.get("contacts")

    @property
    def meeting(self):
        """Get the meeting component"""
        return self.components.get("meeting")

    @property
    def metric(self):
        """Get the metric component"""
        return self.components.get("metric")

    @property
    def report(self):
        """Get the report component"""
        return self.components.get("report")

    @property
    def user(self):
        """Get the user component"""
        return self.components.get("user")

    @property
    def webinar(self):
        """Get the webinar component"""
        return self.components.get("webinar")

    @property
    def recording(self):
        """Get the recording component"""
        return self.components.get("recording")

    @property
    def live_stream(self):
        """Get the live stream component"""
        return self.components.get("live_stream")

    @property
    def phone(self):
        """Get the phone component"""
        return self.components.get("phone")

    @property
    def past_meeting(self):
        """Get the past meeting component"""
        return self.components.get("past_meeting")

    @property
    def group(self):
        """Get the group component"""
        return self.components.get("group")
