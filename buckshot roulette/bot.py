import discord
from discord.ext import commands
from cogs.game_cog import GameCog
from cogs.items_cog import ItemsCog

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
  activity = discord.Game(name="Buckshot Roulette!", type=1)
  await bot.change_presence(status=discord.Status.online, activity=activity)

  game_cogs = GameCog(bot)
  await bot.add_cog(game_cogs)

  items_cogs = ItemsCog(bot, game_cogs.game)
  await bot.add_cog(items_cogs)

bot.run("MTIzMjc1NjM1NjQ2MTg4NzYzMg.GGJrf9.Dg8B32yVKAPVupsuEq5xqg3FHvNqmWaRTiC6ag")