from discord.ext import commands
from models.game import Game
from .game_cog import GameCog

class ItemsCog(commands.Cog):
  def __init__(self, bot, game: Game):
    self.bot = bot
    self.game = game
    self.players = game.players

  def get_current_player(self, ctx):
    return self.players[0] if ctx.author.id == self.players[0].id else self.players[1]

  #hand saw
  @commands.command()
  async def hand_saw(self, ctx):
    if self.game.game_started is False:
      await ctx.send("The game hasn't started yet!")
      return

    turn_id, turn_name = self.game.current_turn()
    player = self.get_current_player(ctx)

    if ctx.author.id != turn_id:
      await ctx.send(f"`It's {turn_name}'s turn!`")
      return

    if "Hand saw" in player.items:
      await ctx.send("`Damage is doubled!`")
      player.damage = 2
      player.items.remove("Hand saw")
    else:
      await ctx.send("`You don't have any Hand saw in your inventory!`")

  #magnifying glass
  @commands.command()
  async def magnifying_glass(self, ctx):
    if self.game.game_started is False:
      await ctx.send("The game hasn't started yet!")
      return

    turn_id, turn_name = self.game.current_turn()
    current_bullet = self.game.bullets[0]
    player = self.get_current_player(ctx)

    if ctx.author.id != turn_id:
      await ctx.send(f"`It's {turn_name}'s turn!`")
      return

    if "Magnifying glass" in player.items:
      await ctx.author.send(f"`Current bullet is {current_bullet}!`")
      player.items.remove("Magnifying glass")
    else:
      await ctx.send("`You don't have any Magnifying glass in your inventory!`")

  #ciggarette pack
  @commands.command()
  async def cigarette_pack(self, ctx):
    if self.game.game_started is False:
      await ctx.send("The game hasn't started yet!")
      return

    turn_id, turn_name = self.game.current_turn()
    player = self.get_current_player(ctx)

    if ctx.author.id != turn_id:
      await ctx.send(f"`It's {turn_name}'s turn!`")
      return

    if "Cigarette pack" in player.items:
      player.lives += 1
      await ctx.send(f"`{player.name}'s current lives: {player.lives}`")
      player.items.remove("Cigarette pack")
    else:
      await ctx.send("`You don't have any Cigarette pack in your inventory!`")

  #handcuffs
  @commands.command()
  async def handcuffs(self, ctx):
    if self.game.game_started is False:
      await ctx.send("The game hasn't started yet!")
      return

    turn_id, turn_name = self.game.current_turn()
    player = self.get_current_player(ctx)

    if ctx.author.id != turn_id:
      await ctx.send(f"`It's {turn_name}'s turn!`")
      return

    if "Handcuffs" in player.items:
      player.extended_round = True
      await ctx.send(f"`{player.name} has extended round!`")
      player.items.remove("Handcuffs")
    else:
      await ctx.send("`You don't have any Handcuffs in your inventory!`")

  #beer
  @commands.command()
  async def beer(self, ctx):
    if self.game.game_started is False:
      await ctx.send("The game hasn't started yet!")
      return

    turn_id, turn_name = self.game.current_turn()
    current_bullet = self.game.bullets[0]
    player = self.get_current_player(ctx)

    if ctx.author.id != turn_id:
      await ctx.send(f"`It's {turn_name}'s turn!`")
      return

    if "Beer" in player.items:
      await ctx.send(f"`Ejected shell was {current_bullet}!`")
      self.game.bullets.pop(0)
      player.items.remove("Beer")
    else:
      await ctx.send("`You don't have any Beer in your inventory!`")