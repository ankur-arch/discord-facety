from dataclasses import dataclass
from typing import List, Optional, Union
from discord.message import Attachment
import numpy as np


@dataclass(frozen=True)
class ImageInfo:
    name: str
    url: str
    type: Optional[str] = None
    numpy_format: Optional[np.ndarray] = None

    @staticmethod
    def from_discord_attachments(attachments: list[Attachment]):
        images: List[ImageInfo] = []

        for attachment in attachments:
            result = ImageInfo.from_discord_attachment(attachment=attachment)
            if result is None:
                continue
            images.append(result)

        return images

    @staticmethod
    def from_discord_attachment(attachment: Attachment):
        supported_formats = ['image/jfif', 'image/jpg',
                             'image/jpeg', 'image/pjp', 'image/pjpeg']

        if attachment.content_type in supported_formats:
            return ImageInfo(name=attachment.filename, url=attachment.url, type=attachment.content_type)
        return None
