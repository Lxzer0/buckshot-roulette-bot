import discord
import os
from discord.ext import commands
from cogs.game_cog import GameCog
from cogs.items_cog import ItemsCog
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_API_TOKEN') or exit('Token not found')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
  activity = discord.Game(name="Buckshot Roulette!", type=1)
  await bot.change_presence(status=discord.Status.online, activity=activity)

  game_cogs = GameCog(bot)
  await bot.add_cog(game_cogs)

  items_cogs = ItemsCog(bot, game_cogs.game)
  await bot.add_cog(items_cogs)

bot.run(TOKEN)