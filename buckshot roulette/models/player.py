import random

class Player: 
  def __init__(self, id, name, lives):
    self.id = id
    self.name = name
    self.lives = lives
    self.damage = 1
    self.items = []
    self.extended_round = False

  def append_item(self, n):
    items = ["Hand saw", "Magnifying glass", "Cigarette pack", "Handcuffs", "Beer"]
    for i in range(n):
      self.items.append(random.choice(items))

  def is_alive(self):
    return self.lives > 0