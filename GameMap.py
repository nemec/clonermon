import pygame.sprite

class Map(pygame.sprite.Group):
  def __init__(self):
    pygame.sprite.Group.__init__(self)

  def update(self, *args, **kwargs):
    for s in self.sprites(): s.update(*args, **kwargs)
