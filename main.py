import disnake
from disnake.ext import commands
from disnake.ext import tasks
from disnake import TextInputStyle
import asyncio
from typing import List
from fuzzywuzzy import process
from PIL import Image
import os
import io
import aiohttp
from dotenv import load_dotenv

load_dotenv()

bot = commands.InteractionBot()

@bot.event
async def on_ready():
    print('Bot is ready.')

class GifType(disnake.ui.Modal):
    def __init__(self, url):
        self.url = url
        components = [disnake.ui.TextInput(label="Enter the GIF type:", placeholder="minecraft", custom_id="type", style=TextInputStyle.short, max_length=14)]
        super().__init__(title="GIF generator", components=components)
    
    async def callback(self, inter: disnake.ModalInteraction) -> None:
        gif_type = inter.text_values["type"].lower()
        
        await inter.response.defer(ephemeral=True)

        if gif_type not in ('abstract', 'ads', 'balls', 'bayer', 'bevel', 'billboard', 'blocks', 'blur', 'boil', 'bomb', 'bonks', 'bubble', 'burn', 'canny', 'cartoon', 'cinema', 'clock', 'cloth', 'contour', 'cow', 'cracks', 'cube', 'dilate', 'dither', 'dots', 'earthquake', 'emojify', 'endless', 'equations', 'explicit', 'fall', 'fan', 'fire', 'flag', 'flush', 'gallery', 'gameboy_camera', 'glitch', 'globe', 'half_invert', 'heart_diffraction', 'hearts', 'infinity', 'ipcam', 'kanye', 'knit', 'lamp', 'laundry', 'layers', 'letters', 'lines', 'liquefy', 'logoff', 'lsd', 'magnify', 'matrix', 'melt', 'minecraft', 'neon', 'optics', 'painting', 'paparazzi', 'patpat', 'pattern', 'phase', 'phone', 'pizza', 'plank', 'plates', 'poly', 'print', 'pyramid', 'radiate', 'rain', 'reflection', 'ripped', 'ripple', 'roll', 'sensitive', 'shear', 'shine', 'shock', 'shoot', 'shred', 'slice', 'soap', 'spikes', 'spin', 'stereo', 'stretch', 'tiles', 'tunnel', 'tv', 'wall', 'warp', 'wave', 'wiggle', 'zonk'):
            await inter.edit_original_response("Wrong GIF type.\nPlease select the GIF type from <https://discord.com/channels/1163511761446637681/1198637019660816394/1223339737813614612>, and make sure to type it correctly.", ephemeral=True)
        else:
            params = {'image_url': self.url}
            headers = {'Authorization': f'Bearer {os.getenv("JEYY_API_KEY")}'}

            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.jeyy.xyz/v2/image/{gif_type}', params=params, headers=headers) as response:
                    buffer = io.BytesIO(await response.read())
                    await asyncio.sleep(6)
                    await inter.edit_original_response(file=disnake.File(buffer, 'output.gif'))

@bot.user_command(name="Gif maker")
async def also_nice(inter: disnake.UserCommandInteraction, user: disnake.User):
    await inter.response.send_modal(modal=GifType(user.display_avatar.url))

gif_types = ['abstract', 'ads', 'balls', 'bayer', 'bevel', 'billboard', 'blocks', 'blur', 'boil', 'bomb', 'bonks', 'bubble', 'burn', 'canny', 'cartoon', 'cinema', 'clock', 'cloth', 'contour', 'cow', 'cracks', 'cube', 'dilate', 'dither', 'dots', 'earthquake', 'emojify', 'endless', 'equations', 'explicit', 'fall', 'fan', 'fire', 'flag', 'flush', 'gallery', 'gameboy_camera', 'glitch', 'globe', 'half_invert', 'heart_diffraction', 'hearts', 'infinity', 'ipcam', 'kanye', 'knit', 'lamp', 'laundry', 'layers', 'letters', 'lines', 'liquefy', 'logoff', 'lsd', 'magnify', 'matrix', 'melt', 'minecraft', 'neon', 'optics', 'painting', 'paparazzi', 'patpat', 'pattern', 'phase', 'phone', 'pizza', 'plank', 'plates', 'poly', 'print', 'pyramid', 'radiate', 'rain', 'reflection', 'ripped', 'ripple', 'roll', 'sensitive', 'shear', 'shine', 'shock', 'shoot', 'shred', 'slice', 'soap', 'spikes', 'spin', 'stereo', 'stretch', 'tiles', 'tunnel', 'tv', 'wall', 'warp', 'wave', 'wiggle', 'zonk']
async def autocomplete_gif_types(inter, string: str) -> List[str]:
    string = string.lower()
    match, _ = process.extractOne(string, gif_types)
    return [match]

@bot.slash_command(name="gifmaker", description="Creates a nice GIF")
async def gifmaker(inter: disnake.ApplicationCommandInteraction, image: disnake.Attachment, type: str = commands.Param(autocomplete=autocomplete_gif_types)):
        """
        Creates a nice GIF

        Parameters
        ----------
        image: Upload the image you need to make a GIF of
        type: Select the GIF type
        """
        await inter.response.defer(ephemeral=True)
        if type.lower() not in gif_types:
            await inter.edit_original_response(content="Wrong GIF type.\nPlease select the GIF type from <https://discord.com/channels/1163511761446637681/1198637019660816394/1223339737813614612>, and make sure to type it correctly.", ephemeral=True)
        else:
            if image.content_type == 'image/webp':
                k = await image.read()
                webp_image = Image.open(io.BytesIO(k))
                png_image = webp_image.convert('RGBA')
                png_buffer = io.BytesIO()
                png_image.save(png_buffer, format='PNG')
                png_buffer.seek(0)
                msg = await inter.author.send("The image is being resent here to obtain it's url, please check the channel where you used your command for your GIF!", file=disnake.File(png_buffer, filename='converted_image.png'))
                imgurl = msg.attachments[0].url
                params = {'image_url': imgurl}
                headers = {'Authorization': f'Bearer {os.getenv("JEYY_API_KEY")}'}
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.jeyy.xyz/v2/image/{type}', params=params, headers=headers) as response:
                        buffer = io.BytesIO(await response.read())
                        await inter.response.defer(ephemeral=True)
                        await asyncio.sleep(6)
                        await inter.edit_original_response(file=disnake.File(buffer, 'output.gif'))
            elif image.content_type.startswith('image'):
                params = {'image_url': image.url}
                headers = {'Authorization': f'Bearer {os.getenv("JEYY_API_KEY")}'}
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.jeyy.xyz/v2/image/{type}', params=params, headers=headers) as response:
                        buffer = io.BytesIO(await response.read())
                        await asyncio.sleep(6)
                        await inter.edit_original_response(file=disnake.File(buffer, 'output.gif'))
            else:
                await inter.edit_original_response(content="The attachment is not an image.", ephemeral=True)

@tasks.loop(count=1)
async def patch_app_commands():
    await bot.wait_until_ready()
    
    for command in bot.global_application_commands:
        print(f"Patching command integration type for {command.id}")
        await bot.http.edit_global_command(
            bot.application_id,
            command.id,
            payload={"integration_types": [1], "contexts": [0, 1, 2]},
        )

patch_app_commands.start()

bot.run(os.getenv("TOKEN"))
