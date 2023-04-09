import dataclasses
from dataclasses import dataclass
from models.image_info import ImageInfo
import httpx
import numpy as np
import asyncio
from io import BytesIO
from PIL import Image
from discord import Attachment
from numpy.lib.type_check import imag


@dataclass
class ImageUtils:
    images: list[ImageInfo]

    async def get(self, client: httpx.AsyncClient, url: str) -> httpx.Response:
        return await client.get(url)

    async def get_images(self) -> list[httpx.Response]:
        client = httpx.AsyncClient()
        response = await asyncio.gather(*[self.get(client, image.url) for image in self.images])
        await client.aclose()
        return response

    @staticmethod
    def from_attachments(attachments: list[Attachment]):
        images = ImageInfo.from_discord_attachments(attachments=attachments)
        return ImageUtils(images=images)

    async def responses_to_numpy(self) -> list[ImageInfo]:
        responses = await self.get_images()
        images_with_numpy_format: list[ImageInfo] = []

        for i, resp in enumerate(responses, 0):
            images_with_numpy_format.append(dataclasses.replace(self.images[i], numpy_format=np.array(
                Image.open(BytesIO(resp.content)))))

        return images_with_numpy_format
