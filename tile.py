from spritesheet import spritesheet
from pygame.locals import *
import pygame.sprite
import pygame.mask
import copy
from itertools import izip_longest
from collections import defaultdict

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

class OverlayTile(Tile):
  def __init__(self, image):
    Tile.__init__(self, image)

class TileSheet(object):
  def __init__(self):
    self.tiles = defaultdict(dict)
    self.aliases = {}
    self.constructs = {}

  # Construct MUST be a rectangle.
  def _build_construct(self, tile_list):
    iw, ih = self.aliases[tiles[0][0]].image.get_size()
    h = len(tile_list)
    w = len(tile_list[0])
    cons = pygame.Surface((w*iw, h*ih))
    types = []
    for row, l in enumerate(tile_list):
      tmprow0 = []
      tmprow1 = []
      for col, image in enumerate(l):
        cons.blit(self.aliases[image].image, (col*iw, row*ih))
        tmprow0.extend(self.aliases[image].type_map[0])
        tmprow1.extend(self.aliases[image].type_map[1])
      types.extend((tuple(tmprow0), tuple(tmprow1)))
    return Tile(cons, tuple(types))

  def get_tile_by_position(self, x, y):
    t = copy.copy(self.tiles[x][y])
    t.rect = t.rect.copy()
    return t

  def get_tile_by_alias(self, tilename):
    return self.get_tile_by_position(*self.aliases[tilename])

  def get_construct(self, construct):
    return copy.copy(self.constructs.get(construct, None))

  def load_from_files(self, tileset_name, tilesize):
    import tile
    ss = spritesheet(tileset_name + ".png", tilesize)
    types = None
    names = None
    with open(tileset_name + ".types", 'r') as types_f:
      types = types_f.readlines()
    with open(tileset_name + ".names", 'r') as names_f:
      names = names_f.readlines()

    if types is None:
      raise ValueError("Could not open types definition, {0}.types".format(tileset_name))

    for x, rows in enumerate(izip_longest(types, names)):
      type_row, name_row = rows
      type_row_tmp = type_row.strip().split(',')
      type_row = []
      for i in type_row_tmp:
        typ, sep, num = i.partition("*")
        if sep != "":
          for n in xrange(int(num)):
            type_row.append(getattr(tile, typ.strip()))
        else:
          type_row.append(getattr(tile, typ.strip()))
  
      if name_row is not None:
        name_row = name_row.strip().split(',')
      else:
        name_row = []
      for y, cols in enumerate(izip_longest(type_row, name_row)):
        type_col, name_col = cols
        typ = type_col(ss.image_pos((y, x)))
        self.tiles[x][y] = typ
        if name_col is not None:
          self.aliases[name_col.strip()] = (x, y)

class Outside(TileSheet):
  def __init__(self):
    super(Outside, self).__init__()
    self.load_from_files("reduced_tileset", 16)
    #ss = spritesheet('reduced_tileset.png', 16)
    """self.aliases = {
      "pebbles" : EmptyTile(ss.image_pos((0,0))),
      "cut_weeds" : EmptyTile(ss.image_pos((1,0))),
      "weeds" : EmptyTile(ss.image_pos((2,0))),
      "plains_1" : EmptyTile(ss.image_pos((3,0))),
      "mowed" : EmptyTile(ss.image_pos((4,0))),
      "flower_1" : EmptyTile(ss.image_pos((5,0))),
      "ul_mountain" : MountainTile(ss.image_pos((6,0))),
      "u_mountain" : MountainTile(ss.image_pos((7,0))),
      "ur_mountain" : MountainTile(ss.image_pos((8,0))),
      "ur_tracks" : EmptyTile(ss.image_pos((9,0))),
      "ul_tracks" : EmptyTile(ss.image_pos((10,0))),


      "l_ledge" : LedgeTile(ss.image_pos((0,1))),

    }"""
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

if __name__ == "__main__":
  import pygame
  pygame.init()
  pygame.display.set_mode((200,200))
  t = TileSheet()
  t.load_from_files("reduced_tileset", 16)

