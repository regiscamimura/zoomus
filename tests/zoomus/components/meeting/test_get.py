import unittest

from zoomus import components, util
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GetV1TestCase))
    suite.addTest(unittest.makeSuite(GetV2TestCase))
    return suite


class GetV1TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponent(
            base_uri="http://foo.com",
            config={
                "account_id": "KEY",
                "client_id": "CLIENT_ID",
                "client_secret": "CLIENT_SECRET",

                "version": util.API_VERSION_1,
            },
        )

    @responses.activate
    def test_can_get(self):
        responses.add(
            responses.POST,
            "http://foo.com/meeting/get?id=ID&host_id=ID&account_id=KEY&client_id=SECRET",
        )
        self.component.get(id="ID", host_id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.get()

    def test_requires_host_id(self):
        with self.assertRaisesRegexp(ValueError, "'host_id' must be set"):
            self.component.get(id="ID")


class GetV2TestCase(unittest.TestCase):
    def setUp(self):
        self.component = components.meeting.MeetingComponentV2(
            base_uri="http://foo.com",
            config={
                "account_id": "KEY",
                "client_id": "CLIENT_ID",
                "client_secret": "CLIENT_SECRET",

                "version": util.API_VERSION_2,
            },
        )

    @responses.activate
    def test_can_get(self):
        responses.add(responses.GET, "http://foo.com/meetings/ID")
        self.component.get(id="ID")

    def test_requires_id(self):
        with self.assertRaisesRegexp(ValueError, "'id' must be set"):
            self.component.get()


if __name__ == "__main__":
    unittest.main()
