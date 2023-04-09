import io
import discord
from recognizer import analyzeFace
from image_utils import ImageUtils
import os
from discord import Client
from discord.flags import Intents
from discord.message import Message

import dotenv
dotenv.load_dotenv()


TOKEN = os.environ.get('TOKEN')
intents = Intents().all()

bot = Client(intent=intents)


@bot.event
async def on_ready():
    print('Bot is ready')


@bot.event
async def on_message(message: Message):

    # return if the user is the bot because
    if(message.author.bot):
        return

    # receive images from a user in any channel
    if message.attachments:

        await message.channel.send('Bot is processing the images')

        image_group = ImageUtils.from_attachments(message.attachments)
        images = await image_group.responses_to_numpy()

        for faces in analyzeFace(images):
            if faces:
                await message.add_reaction(
                    faces.emotion_emoji())
                try:
                    data = io.BytesIO(faces.face)
                    await message.channel.send(f'```python\nDear {message.author.display_name}\n The race of the person is most likely {faces.race} and age is {faces.age}. The person seems to be {faces.emotion}```',
                                               file=discord.File(
                                                   data, 'person.png')
                                               )
                except:
                    print('Something went wrong')
                    await message.channel.send(f'Something went wrong, I\'m sorry {message.author.display_name}')

    print('Message received and processed')


bot.run(TOKEN)
