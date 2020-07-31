""" Defintions of all objects required to communicate with
the W24 Techread API.
"""
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import UUID4, BaseModel, HttpUrl, Json

from .ask import W24Ask, W24AskType


class W24TechreadAction(str, Enum):
    """ List of supported actions by the Techread API
    """
    INITIALIZE = "INITIALIZE"
    READ = "READ"


class W24TechreadCommand(BaseModel):
    """ Command that is sent from the client to the Server
    """
    action: W24TechreadAction
    message: Json


class W24TechreadMessageType(str, Enum):
    """ Message Type of the message that is sent
    from the server to the client in response to
    a request.
    """
    ASK = "ASK"
    ERROR = "ERROR"
    PROGRESS = "PROGRESS"
    REJECTION = "REJECTION"


class W24TechreadMessageSubtypeError(str, Enum):
    """ Message Subtype for the MessageType: ERROR
    """
    INTERNAL = "INTERNAL"


class W24TechreadMessageSubtypeRejection(str, Enum):
    """ Message Subtype for the MessageType: REJECTION
    """
    COMPLEXITY_EXCEEDED = "COMPLEXITY_EXCEEDED"
    PAPER_SIZE_LIMIT_EXCEEDED = "PAPER_SIZE_LIMIT_EXCEEDED"


class W24TechreadMessageSubtypeProgress(str, Enum):
    """ Message Subtype for the MessageType: PROGRESS
    """
    INITIALIZATION_SUCCESS = "INITIALIZATION_SUCCESS"
    COMPLETED = "COMPLETED"
    STARTED = "STARTED"


W24TechreadMessageSubtypeAsk = W24AskType
""" The MessageType: ASK will return the subtypes
defined in W24AskTypes
"""

W24TechreadMessageSubtype = Union[
    W24TechreadMessageSubtypeError,
    W24TechreadMessageSubtypeProgress,
    W24TechreadMessageSubtypeAsk]
""" Shorthand to summorize all the supported
MessageTypes
"""


class W24TechreadMessage(BaseModel):
    """ Message format for messages that are send
    from the server to the client.
    """
    request_id: UUID4
    """ unique UUID4 that is generated by the
    server to identify the request
    """

    message_type: W24TechreadMessageType
    """ Main Message Type (see W24TechreadMessageType)
    """

    message_subtype: W24TechreadMessageSubtype
    """ Message SubType (see W24TechreadMessageSubtype)
    """

    payload_dict: Optional[Dict] = None
    """ Payload dictionary containing the response
    as dict. The MessageType/Subtype will tell the
    interpreter how to turn the payload back into
    the corresponding object
    """

    payload_url: Optional[HttpUrl] = None
    """ For binary data, the API will return a download
    url which carries the data. This allows us to transfer
    larger images etc.
    """

    payload_bytes: Optional[bytes] = None
    """ Binary reference of the payload. This will only
    become available after the client has downloaded the
    payload_url.
    """


class W24TechreadRequest(BaseModel):
    """ Definition of a W24DrawingReadRequest containing
    all the asks (i.e., things you want to learn about
    the technical drawing).

    """
    asks: List[W24Ask] = []
    """ List of asks """

    development_key: Optional[str] = None
    """ The development_key is used for internal purposes.
    It wil give you access to pre-release versions of our software.
    You will only understand the details if you
    """
