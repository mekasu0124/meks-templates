import disnake
import os
import json
import asyncio

from disnake.ext import commands
from createDb import create_db

"""
open the config.json file, and obtain the values token_live, token_dev, dev_mode
and then iterate through the guild ids you placed in the guild_ids dictionary
and store them in a list for later iteration and loading.
"""
with open('./config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

token_live = data["token_live"]
token_dev = data["token_dev"]
dev_mode = data["dev_mode"]
guild_ids = []

for i in data["guild_ids"].keys():
    iden = data["guild_ids"][i]
    guild_ids.append(iden)

# initialize the bots intentions
# for more information, please see https://docs.disnake.dev/en/latest/api.html?highlight=intent#disnake.Intents
intents = disnake.Intents.all()

# if you have two separate bots, and want to give each one it's own command prefix
if dev_mode == "True":
    bot = commands.Bot(command_prefix='>>',intents=intents,guild_ids=guild_ids,sync_commands_debug=True)
else:
    bot = commands.Bot(command_prefix='<<',intents=intents,guild_ids=guild_ids,sync_commands_debug=True)


# otherwise, uncomment line below and delete 4 lines above.
# bot = commands.Bot(command_prefix='>>',intents=intents,guild_ids=guild_ids,sync_commands_debug=True)

@bot.event
async def on_ready():
    # iterate through guilds bot is in
    for guild in bot.guilds:
        # obtain terminal channel
        term_channel = disnake.utils.get(guild.text_channels, name="gawther_terminal")
        # set a counter
        count = 0
        # iterate through cogs
        for filename in os.listdir('./cogs'):
            # find one, if any
            if filename.endswith('py'):
                # load it
                bot.load_extension(f'cogs.{filename[:-3]}')
                # count it
                count += 1
                # tell it
                await term_channel.send(f'{filename} loaded')

        # delete all the _tell it_'s from above
        await term_channel.purge(limit=count)

        # check dev_mode
        if dev_mode == "True":
            # tell it
            msg = await term_channel.send(f'{bot.user} Logging In - Dev Mode Enabled')
            # sleep it
            await asyncio.sleep(0.5)
            # delete it
            await msg.delete()
            # tell it again
            await term_channel.send(f'{bot.user} Has Logged In - Dev Mode Enabled')
            # end function
            return
        else:
            # tell it
            msg = await term_channel.send(f'{bot.user} Logging In - Dev Mode Disabled')
            # sleep it
            await asyncio.sleep(0.5)
            # delete it
            await msg.delete()
            # tell it again
            await term_channel.send(f'{bot.user} Has Logged In - Dev Mode Disabled')
            # end function
            return


# credit for this update command goes to
# gamingbuddhist#9599 - discord
@bot.command()
@commands.is_owner()
async def update(ctx):
    async def start():
        os.system("python ./bot.py")
        await confirm()
    await ctx.send("Gawther will reset now")
    await start()

async def confirm(ctx):
    await ctx.send("Restart Complete")


if __name__ == '__main__':
    # create your database
    create_db()

    # check dev mode again
    if dev_mode == "True":
        # load dev bot
        bot.run(token_dev)
    else:
        # load live bot
        bot.run(token_live)