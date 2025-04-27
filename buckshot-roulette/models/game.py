import random

class Game:
  def __init__(self):
    self.players = []
    self.bullets = []
    self.game_started = False
    self.turn = None

  def load_bullets(self):
    self.bullets = ["live"] * random.randint(1, 4) + ["blank"] * random.randint(1, 4)
    random.shuffle(self.bullets)

  def count_bullets(self):
    live_bullets = self.bullets.count('live')
    blanks = self.bullets.count('blank')

    return live_bullets, blanks

  def current_turn(self):
    if not self.turn:
      return None, None

    return self.turn.id, self.turn.name

  def change_turn(self, extended):
    if extended:
      return

    self.turn = self.players[1] if self.turn == self.players[0] else self.players[0]

  def is_over(self):
    return not self.players[0].is_alive() or not self.players[1].is_alive()