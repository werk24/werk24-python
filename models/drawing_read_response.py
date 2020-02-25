from pydantic import BaseModel, UUID4
from .payload import W24Payload


class W24DrawingReadResponse(BaseModel):
    request_id: UUID4
    payload: W24Payload
