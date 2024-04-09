import discord
import json
import ast
from discord import app_commands as app

with open("./token.json") as tokenfile:
    token = json.load(tokenfile)["puffer"]

bot = discord.Client(intents=discord.Intents.all())
tree = app.CommandTree(bot)

guild = discord.Object(id=1226549383781290205)

def is_admin(ctx: discord.Interaction):
    return ctx.user.guild_permissions.administrator

def is_dev(ctx: discord.Interaction):
    return ctx.user.id == 450678229192278036

@bot.event
async def on_ready():
    await tree.sync(guild=guild)

    channel = bot.get_channel(1226549384397979784)
    await channel.send(f"**Puffer** is now running on **discord.py {discord.__version__}**!")

@tree.command(name="ping", description="Is the bot alive?", guild=guild)
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message("pong :3")

@tree.command(name="exec", description="Creates a message with an embed.", guild=guild)
@app.check(is_dev)
async def execute(ctx: discord.Interaction, code: str):
    runner = compile(code, "user_input", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    coro: Awaitable | None = eval(runner)
    if coro is not None: await coro

bot.run(token)