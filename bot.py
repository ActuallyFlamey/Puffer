import discord
import json
from discord import app_commands as app

with open("./token.json") as tokenfile:
    token = json.load(tokenfile)["puffer"]

bot = discord.Client(intents=discord.Intents.default())
tree = app.CommandTree(bot)

guild = discord.Object(id=1226549383781290205)

def is_admin(ctx: discord.Interaction):
    return ctx.user.guild_permissions.administrator

@bot.event
async def on_ready():
    await tree.sync(guild=guild)

@tree.command(name="ping", description="Is the bot alive?", guild=guild)
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message("pong :3")

@tree.command(name="mkembed", description="Creates a message with an embed.", guild=guild)
@app.check(is_admin)
async def mkembed(ctx: discord.Interaction, title: str, description: str=None, color: str=None, thumbnail: str=None, fields: str=None):
    if color is not None: color = int(color, 16)

    e = discord.Embed(title=title, color=color, description=description)
    if thumbnail is not None: e.set_thumbnail(url=thumbnail)

bot.run(token)