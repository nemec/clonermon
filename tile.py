from spritesheet import spritesheet
from multimethod import multimethod
from pygame.locals import *
import pygame.sprite
import pygame.mask
import copy

class Tile(pygame.sprite.Sprite):
  def __init__(self, image):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.rect = image.get_rect()

  def get_blit(self):
    return (self.image, self.rect)

  def update(self, *args, **kw):
    if 'increment' in kw and 'direction' in kw:
      # These directions are opposite of what's expected, since the
      # map moves down instead of the player moving up
      if kw['direction'] == K_UP:
        self.rect = self.rect.move(0, kw['increment'])
      elif kw['direction'] == K_DOWN:
        self.rect = self.rect.move(0, -kw['increment'])
      elif kw['direction'] == K_LEFT:
        self.rect = self.rect.move(kw['increment'], 0)
      elif kw['direction'] == K_RIGHT:
        self.rect = self.rect.move(-kw['increment'], 0)

class EmptyTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class SolidTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class EntranceTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class WaterTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class InteractTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class GrassTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class LedgeTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class MountainTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class StepTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class TileSheet(object):
  def __init__(self):
    self.inner_tile = {}
    self.constructs = {}

  # Construct MUST be a rectangle.
  def _build_construct(self, tiles):
    iw, ih = self.inner_tile[tiles[0][0]].image.get_size()
    h = len(tiles)
    w = len(tiles[0])
    cons = pygame.Surface((w*iw, h*ih))
    types = []
    for row, l in enumerate(tiles):
      tmprow0 = []
      tmprow1 = []
      for col, image in enumerate(l):
        cons.blit(self.inner_tile[image].image, (col*iw, row*ih))
        tmprow0.extend(self.inner_tile[image].type_map[0])
        tmprow1.extend(self.inner_tile[image].type_map[1])
      types.extend((tuple(tmprow0), tuple(tmprow1)))
    return Tile(cons, tuple(types))

  def get_tile(self, tilename):
    return copy.copy(self.inner_tile.get(tilename, None))

  def get_construct(self, construct):
    return copy.copy(self.constructs.get(construct, None))

class Outside(TileSheet):
  def __init__(self):
    super(Outside, self).__init__()
    ss = spritesheet('reduced_tileset.png', 16)
    self.inner_tile = {
      "pebbles" : EmptyTile(ss.image_pos((0,0))),
      "ledge"   : LedgeTile(ss.image_pos((0,1))),

    }
    self.constructs = {
      #"gym" : self._build_construct(
      #          (("twostory_lslope", "twostory_croof", "twostory_rslope"),
      #           ("gym_lbottom"    , "gym_cbottom"   , "gym_rbottom"    ))
      #        ),
    }

class Inside(TileSheet):
  pass

class Cave(TileSheet):
  pass

