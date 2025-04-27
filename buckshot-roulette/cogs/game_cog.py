from discord.ext import commands
from models.player import Player
from models.game import Game
import random

class GameCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.game = Game()
    self.lives = random.randint(2,5)

  @commands.command()
  async def join(self, ctx, name):
    for player in self.game.players:
      if player.id == ctx.author.id or player.name == name:
        await ctx.send("You already joined or the nickname is already used!")
        return

    if len(self.game.players) < 2:
      self.game.players.append(Player(ctx.author.id, name, self.lives))
      await ctx.send(f"{name} has joined as player {len(self.game.players)}!")

    if len(self.game.players) == 2:
      await self.start_game(ctx)

  async def start_game(self, ctx):
    global player1, player2
    player1 = self.game.players[0]
    player2 = self.game.players[1]
    for player in self.game.players:
      player.append_item(2)

    self.game.turn = random.choice(self.game.players)
    self.game.load_bullets()
    self.game.game_started = True

    live_bullets, blanks = self.game.count_bullets()
    turn_id, turn_name = self.game.current_turn()

    await ctx.send("```Game has been created!\n"
    f"Players: {player1.name} and {player2.name}\n"
    f"Live bullets: {live_bullets}, Blanks: {blanks}\n"
    f"Current turn: {turn_name}\n"
    f"{player1.name}:\n"
    f"  Lives: {player1.lives}\n"
    f"  Items: {', '.join(player1.items) if player1.items else 'No items'}\n"
    f"{player2.name}:\n"
    f"  Lives: {player2.lives}\n"
    f"  Items: {', '.join(player2.items) if player2.items else 'No items'}```")

  @commands.command()
  async def shoot(self, ctx, name):
    if self.game.game_started is False:
      await ctx.send("The game hasn't started yet!")
      return

    turn_id, turn_name = self.game.current_turn()
    author_id = ctx.author.id
    current_bullet = self.game.bullets[0]

    if author_id != turn_id:
      await ctx.send(f"`It's {turn_name}'s turn!`")
      return

    players = { player1.name: player1, player2.name: player2 }
    victim = players.get(name)
    shooter = player1 if author_id == player1.id else player2

    if victim is None:
      await ctx.send("`Provided name seems incorrect!`")
      return

    if current_bullet == "live":
      await ctx.send("`Live!`")
      victim.lives -= shooter.damage
      await ctx.send(f"```{victim.name} was shot!\n"
      f"Remaining lives: {victim.lives}```")
      self.game.change_turn(shooter.extended_round)

    elif current_bullet == "blank":
      await ctx.send("`Blank!`")
      if shooter != victim:
        self.game.change_turn(shooter.extended_round)

    shooter.extended_round = False
    shooter.damage = 1
    self.game.bullets.pop(0)

    if self.game.is_over():
      winner = player1.name if player1.lives > 0 else player2.name
      await ctx.send(f"**Game over! {winner} has won!**")
      return
      
    if not self.game.bullets:
      await self.next_round(ctx)
      return
    
    turn_id, turn_name = self.game.current_turn()
    await ctx.send(f"`Next turn: {turn_name}`")

  async def next_round(self, ctx):
    await ctx.send("`No bullets left! Next round!`")
    
    self.game.load_bullets()
    live_bullets, blanks = self.game.count_bullets()
    turn_id, turn_name = self.game.current_turn()
    
    for player in self.game.players:
      if len(player.items) < 7:
        player.append_item(2)

    await ctx.send(f"```Live bullets: {live_bullets}, Blanks: {blanks}\nCurrent turn: {turn_name}```")

    for player in self.game.players:
      await ctx.send(f"```{player.name}:\n"
      f"  Lives: {player.lives}\n"
      f"  Items: {', '.join(player.items) if player.items else 'No items'}```")

  @commands.command()
  async def stats(self, ctx):
    if self.game.game_started is False:
      await ctx.send("The game hasn't started yet!")
      return

    for player in self.game.players:
      await ctx.send(f"```{player.name}:\n"
      f"  Lives: {player.lives}\n"
      f"  Items: {', '.join(player.items) if player.items else 'No items'}```")
      
  @commands.command()
  async def reset(self, ctx):
    self.game.players = []
    self.game.bullets = []
    self.game.game_started = False
    self.game.turn = None
    await ctx.send("The game has been reset!")

  @commands.command()
  async def info(self, ctx):
    await ctx.send("```Buckshot Roulette is a modified game of Russian roulette.\n"
    "Every game session players get certain amount of lives 3-5).\n"
    "At the start of each round Dealer loads the shotgun with a certain amount of live shells and blanks in a random order.\n"
    "Each round players get 2 random items which can be used in their favor.\n"
    "The player then chooses to either shoot the opponent or themselves.\n"
    "Depending on whether the player chooses to shoot themselves or the opponent,\n"
    "if the shell is live, then either the player or the opponent loses a life,\n"
    "but if the shell is blank, the player either continues their turn or the shotgun goes to the opponent.\n"
    "\ncommands:\n"
    "!join *name* - join to the game as a player!\n"
    "!stats - displays current information about players!\n"
    "!hand_saw - which converts the shotgun into a sawed-off shotgun that takes two charges if the shell is live!\n"
    "!magnifying_glass - magnifying glass, which reveals the shell currently loaded in the shotgun!\n"
    "!cigarette_pack - which restores one life!\n"
    "!handcuffs - which forces the opponent to skip their next turn!\n"
    "!beer - which safely racks the shotgun, ejecting the loaded shell without consequences!\n"
    "!shoot *name* - shoot, name references to person who will be shooted!\n```")