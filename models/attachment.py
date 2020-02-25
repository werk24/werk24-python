import base64
import hashlib

from pydantic import BaseModel


class W24Attachment(BaseModel):
    """ W24Attachment describes the details of an attachment.
    This is currently only used to attach images (e.g. of renderings
    or extracts from the sheet).
    """
    attachment_hash: str
    content_b64: str

    @classmethod
    def from_bytes(cls, content: bytes) -> 'W24Attachment':
        """ Create a new W24 Image instance directly from the bytes of
        a PNG file
        """
        content_b64 = base64.b64encode(content)
        print(type(content_b64))
        exit()
        attachment_hash = cls.make_attachment_hash(content_b64)
        return W24Attachment(
            attachment_hash=attachment_hash,
            content_b64=content_b64)

    @staticmethod
    def make_attachment_hash(content_b64: str) -> str:
        return hashlib.sha256(content_b64.encode("utf-8")).hexdigest()


W24Attachment.update_forward_refs()