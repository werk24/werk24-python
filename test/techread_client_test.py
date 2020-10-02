from uuid import UUID

import aiounittest
from werk24.models.ask import W24AskPageThumbnail
from werk24.exceptions import LicenseError, UnauthorizedException
from werk24.models.techread import (W24AskType,
                                    W24TechreadMessageSubtypeProgress,
                                    W24TechreadMessageType)
from werk24.techread_client import W24TechreadClient

from .utils import CWD, get_drawing

LICENSE_PATH_INVALID_CREDS = CWD / "assets" / "invalid_creds.werk24"
""" Path to the license file with invalid credentials """

DRAWING = get_drawing()
""" Example Drawing in bytes """


class TestTechreadClient(aiounittest.AsyncTestCase):
    """ Test case for the basic Techread functionality
    """

    def test_license_path_invalid(self):
        """ Test Invalid License Path

        User Story: As API user, I want to obtain an exception
            if the path that I provided to the license file is
            invalid, so that I can detect problems before they
            go into production.
        """
        self.assertRaises(
            LicenseError,
            W24TechreadClient.make_from_env,
            license_path="invalid_path")

    async def test_license_invalid(self):
        """ Test Invalid License File

        User Story: As API user, I want to obtain an exception
            when the license that I supplied is invalid, so that
            I know that the license expired / was disabled / ...
        """
        client = W24TechreadClient.make_from_env(
            license_path=LICENSE_PATH_INVALID_CREDS)

        with self.assertRaises(UnauthorizedException):
            async with client:
                pass

    async def test_read_drawing(self):
        """ Test basic read_drawing functionality

        User Story: As API user, I want to initiate a basic
        read request to verify that the basic functionality
        works
        """

        client = W24TechreadClient.make_from_env(None)
        async with client as session:
            request = session.read_drawing(DRAWING, [W24AskPageThumbnail()])

            # check whether the first message give us the state information
            message_first = await request.__anext__()
            self.assertEqual(type(message_first.request_id), UUID)
            self.assertEqual(message_first.message_type,
                             W24TechreadMessageType.PROGRESS)
            self.assertEqual(message_first.message_subtype,
                             W24TechreadMessageSubtypeProgress.STARTED)

            # check whether the second message gives us the information
            # about the requested thumbnail
            message_second = await request.__anext__()
            self.assertEqual(message_second.message_type,
                             W24TechreadMessageType.ASK)
            self.assertEqual(message_second.message_subtype,
                             W24AskType.PAGE_THUMBNAIL)
            self.assertGreater(len(message_second.payload_bytes), 0)

            # check whether we close the iteration correctly
            with self.assertRaises(StopAsyncIteration):
                await request.__anext__()
