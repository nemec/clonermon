import pygame
from pygame.locals import *

class Character(pygame.sprite.Sprite):
  def __init__(self, front, back=None, left=None, right=None):
    pygame.sprite.Sprite.__init__(self)
    self.default = front
    self.animated = False
    self.direction = K_DOWN
    self.image = self.default
    self.rect = self.image.get_rect()
    if left and not right:
      right = pygame.transform.flip(left, True, False)
    self.standing = {K_UP:back, K_DOWN:front, K_LEFT:left, K_RIGHT:right}
    self.animation = None
    self.update_dir = None

  def set_animated(self, animup, animdown, animleft, animright = None):
    if not animright:
      animright = pygame.transform.flip(animleft, True, False)
    self.animation = {K_UP:animup, K_DOWN:animdown,
                      K_LEFT:animleft, K_RIGHT:animright}
    self.animated = True
    
    return

  def animate(self, on):
    # Has no effect if the character is not animated.
    if not self.animated:
      return
    if on:
      if self.animation:
        self.image = self.animation[self.direction]
    else:
      self.image = self.standing.get(self.direction, self.default)

  def will_move(self, direction):
    if self.direction == direction:
      return True
    elif direction in self.standing:
      self.direction = direction
      self.update_dir = direction
      return False
    else:
      return False

  def update(self, *args):
    if self.update_dir:
      direction = self.update_dir
      self.image = self.standing.get(self.direction, self.default)
    self.update_dir = None

class Player(Character):
  pass

class NPC(Character):
  pass
