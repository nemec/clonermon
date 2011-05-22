import os
import pygame
import pygame.sprite
from pygame.locals import *

import tile
import character
import collision

class Screen(object):
  def __init__(self, width=160, height=144, tilesize = 16):
    if width % tilesize != 0 or height % tilesize != 0:
      raise ValueError("Tile size must be multiple of width and height.")
    self.tilesize = tilesize
    self.screen = pygame.display.set_mode((width,height))
    self.bg_surface = pygame.Surface(self.screen.get_size())
    self.bg_surface.fill((0,255,0))
    self.player = None
    self.background = Map()
    self.interactions = Map()
    self.characters = Map()
    self.overlay = Map()
    self.collidable = (self.background, self.interactions, self.characters)
    self.layers = (self.background, self.interactions,
                  self.characters, self.overlay)

  def update(self, *args, **kwargs):
    for layer in self.layers:
      layer.update(*args, **kwargs)
    
    self.player.update(self.background)

  def draw(self):
    self.screen.blit(self.bg_surface, (0,0))
    for layer in self.layers:
      layer.draw(self.screen)
    self.player.draw(self.screen)

  def __iter__(self):
    """ Iterate over every collisionable layer """
    for layer in self.collidable:
      for i in layer:
        yield i

  def set_player(self, player):
    height, width = self.screen.get_size()
    posx = int(((height/self.tilesize)-1)/2) * self.tilesize
    posy = int(((width/self.tilesize)-1)/2) * self.tilesize
    player.rect.move_ip(posx, posy)
    self.player = pygame.sprite.RenderPlain(player)

  def add(self, t, loc = None):
    if loc is not None:
      loc = map(lambda x: x * self.tilesize, loc)
      t.rect.move_ip(loc)
    if isinstance(t, tile.InteractTile):
      self.interactions.add(t)
    elif isinstance(t, tile.OverlayTile):
      self.overlay.add(t)
    elif isinstance(t, tile.Tile):
      self.background.add(t)
    elif isinstance(t, character.Player):
      pass # can't change players!
    elif isinstance(t, character.Character):
      self.characters.add(pygame.sprite.RenderPlain(t))

  def get_adjacent_tile(self, curr_tile, direction):
    rect = None
    if direction == K_UP:
      rect = curr_tile.rect.move(0, -self.tilesize)
    elif direction == K_DOWN:
      rect = curr_tile.rect.move(0, self.tilesize)
    elif direction == K_LEFT:
      rect = curr_tile.rect.move(-self.tilesize, 0)
    elif direction == K_RIGHT:
      rect = curr_tile.rect.move(self.tilesize, 0)
    if rect is None:
      return None

    for layer in self.collidable:
      for x in layer:
        if rect.colliderect(x.rect):
          return x
    return None


class Map(pygame.sprite.Group):
  def __init__(self):
    pygame.sprite.Group.__init__(self)

  def update(self, *args, **kwargs):
    for s in self.sprites(): s.update(*args, **kwargs)

  def load_from_file(self, filename):
    data = None
    with open(filename, 'r') as f:
      data = f.readlines()
    if data is not None:
      i = iter(data)
      info = i.next().split(",")
      if len(info) != 6:
        raise ValueError("Need five values on first line of map file.")
      tsheet = tile.TileSheet()
      tilesheet_name = info[0][info[0].rfind(os.sep)+1:].strip()
      tilesize = int(info[1])
      tsheet.load_from_files(tilesheet_name, tilesize)
      for raw_t in i:
        t = raw_t.split(",")
        mapx, mapy, tilex, tiley = map(int, t)
        t = tsheet.get_tile_by_position(tilex, tiley)
        t.rect.move_ip(mapx * tilesize, mapy * tilesize)
        self.add(t)

if __name__ == "__main__":
  import pygame
  pygame.init()
  pygame.display.set_mode((200,200))
  m = Map()
  m.load_from_file("mapbuilder/new_map.map")
