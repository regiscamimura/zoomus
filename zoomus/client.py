"""Zoom.us REST API Python Client"""

from __future__ import absolute_import, unicode_literals

from zoomus import components, util
from zoomus.util import API_VERSION_1, API_VERSION_2, API_GDPR


API_BASE_URIS = {
    API_VERSION_1: "https://api.zoom.us/v1",
    API_VERSION_2: "https://api.zoom.us/v2",
    API_GDPR: "https://eu01api-www4local.zoom.us/v2",
}

COMPONENT_CLASSES = {
    API_VERSION_1: {
        "meeting": components.meeting.MeetingComponent,
        "recording": components.recording.RecordingComponent,
        "report": components.report.ReportComponent,
        "user": components.user.UserComponent,
        "webinar": components.webinar.WebinarComponent,
    },
    API_VERSION_2: {
        "contacts": components.contacts.ContactsComponentV2,
        "group": components.group.GroupComponentV2,
        "live_stream": components.live_stream.LiveStreamComponentV2,
        "meeting": components.meeting.MeetingComponentV2,
        "metric": components.metric.MetricComponentV2,
        "past_meeting": components.past_meeting.PastMeetingComponentV2,
        "phone": components.phone.PhoneComponentV2,
        "recording": components.recording.RecordingComponentV2,
        "report": components.report.ReportComponentV2,
        "room": components.room.RoomComponentV2,
        "user": components.user.UserComponentV2,
        "webinar": components.webinar.WebinarComponentV2,
    },
}


class ZoomClient(util.ApiClient):
    """Zoom.us REST API Python Client"""

    """Base URL for Zoom API"""

    def __init__(
        self,
        account_id,
        client_id,
        client_secret,
        data_type="json",
        timeout=15,
        version=API_VERSION_2,
        base_uri=None,
    ):
        """Create a new Zoom client

        :param account_id: The Zooom.us app account id
        :param client_id: The Zoom.us app client_id 
        :param client_secret: The Zoom.us app client secret
        :param data_type: The expected return data type. Either 'json' or 'xml'
        :param timeout: The time out to use for API requests
        :param version: The API version to use (Default is V2). The available
                        options are API_VERSION_1 (deprecated by Zoom),
                        or API_VERSION_2 (default)
        :param base_uri: Set the base URI to use. By default this is chosen
                         based on the API version chosen, but it can be
                         overriden so that the GDPR compliant base URI can
                         be used in the EU.
        """
        try:
            base_uri = base_uri or API_BASE_URIS[version]
            self.components = COMPONENT_CLASSES[version].copy()
        except KeyError:
            raise RuntimeError("API version not supported: %s" % version)

        super(ZoomClient, self).__init__(base_uri=base_uri, timeout=timeout)

        # Setup the config details
        self.config = {
            "account_id": account_id,
            "client_id": client_id,
            "client_secret": client_secret,
            "data_type": data_type,
            "version": version,
            "base_uri": base_uri,
            "token": util.generate_access_token(account_id, client_id, client_secret),
        }

        # Instantiate the components
        for key in self.components.keys():
            self.components[key] = self.components[key](
                base_uri=base_uri, config=self.config
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def refresh_token(self):
        self.config["token"] = (
            util.generate_access_token(
                self.config["account_id"],
                self.config["client_id"],
                self.config["client_secret"],
            ),
        )

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

    @property
    def room(self):
        """Get the room component"""
        return self.components.get("room")
