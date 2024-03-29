import disnake
from disnake.ext import commands
from disnake.ext import tasks
from disnake import TextInputStyle
import re
import asyncio
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
        components = [disnake.ui.TextInput(label="Enter the GIF type:", placeholder="youtube", custom_id="type", style=TextInputStyle.short, max_length=14)]
        super().__init__(title="GIF generator", components=components)
    
    async def callback(self, inter: disnake.ModalInteraction) -> None:
        gif_type = inter.text_values["type"].lower()
        
        if gif_type not in ('abstract', 'ads', 'balls', 'bayer', 'bevel', 'billboard', 'blocks', 'blur', 'boil', 'bomb', 'bonks', 'bubble', 'burn', 'canny', 'cartoon', 'cinema', 'clock', 'cloth', 'contour', 'cow', 'cracks', 'cube', 'dilate', 'dither', 'dots', 'earthquake', 'emojify', 'endless', 'equations', 'explicit', 'fall', 'fan', 'fire', 'flag', 'flush', 'gallery', 'gameboy_camera', 'glitch', 'globe', 'half_invert', 'heart_diffraction', 'hearts', 'infinity', 'ipcam', 'kanye', 'knit', 'lamp', 'laundry', 'layers', 'letters', 'lines', 'liquefy', 'logoff', 'lsd', 'magnify', 'matrix', 'melt', 'minecraft', 'neon', 'optics', 'painting', 'paparazzi', 'patpat', 'pattern', 'phase', 'phone', 'pizza', 'plank', 'plates', 'poly', 'print', 'pyramid', 'radiate', 'rain', 'reflection', 'ripped', 'ripple', 'roll', 'sensitive', 'shear', 'shine', 'shock', 'shoot', 'shred', 'slice', 'soap', 'spikes', 'spin', 'stereo', 'stretch', 'tiles', 'tunnel', 'tv', 'wall', 'warp', 'wave', 'wiggle', 'zonk'):
            await inter.response.send_message("Wrong GIF type.\nPlease select the GIF type from <https://discord.com/channels/1163511761446637681/1198637019660816394/1223339737813614612>, and make sure to type it correctly.", ephemeral=True)
        else:
            params = {'image_url': self.url}
            headers = {'Authorization': f'Bearer {os.getenv("JEYY_API_KEY")}'}

            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.jeyy.xyz/v2/image/{gif_type}', params=params, headers=headers) as response:
                    buffer = io.BytesIO(await response.read())
                    await inter.response.defer(ephemeral=True)
                    await asyncio.sleep(10)
                    await inter.edit_original_response(file=disnake.File(buffer, 'output.gif'))

image_extensions_pattern = r'\.(jpg|jpeg|png|gif|)$'

@bot.message_command(name="Gif generator")
async def gif_gen(inter: disnake.MessageCommand, message: disnake.Message):
    if message.attachments:
        attachment = message.attachments[0]
        if attachment.content_type.startswith('image'):
            url = attachment.url
            modal = GifType(url)
            await inter.response.send_modal(modal=modal)
        else:
            await inter.response.send_message("The attachment is not an image or a GIF.", ephemeral=True)
    else:
        if message.content:
            urls = re.findall(r'(https?://\S+)', message.content)
            if urls:
                for url in urls:
                    if re.search(image_extensions_pattern, url, re.IGNORECASE):
                        modal = GifType(url)
                        await inter.response.send_modal(modal=modal)
                        break
                else:
                    await inter.response.send_message("No valid image or GIF link found in the message content.", ephemeral=True)
            else:
                await inter.response.send_message("No URLs found in the message content.", ephemeral=True)
        else:
            await inter.response.send_message("No attachment or message content found.", ephemeral=True)

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