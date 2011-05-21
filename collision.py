import pygame.sprite
from multimethod import SymmetricTravel, multimethod
from tile import *

def sprite_collision(player, tile):
  if pygame.sprite.collide_rect(player, tile):
    print player.current_tile
    return not can_enter(player.current_tile,tile)
  return False

@SymmetricTravel(EmptyTile, GrassTile, StepTile)
def can_enter(fro, to):
  return True

@multimethod(EntranceTile, EmptyTile)
def can_enter(fro, to):
  return True

@multimethod(EmptyTile, WaterTile)
def can_enter(fro, to):
  return False

@multimethod(WaterTile, GrassTile, StepTile, EmptyTile,
                                              rootto=True)
def can_enter(fro, to):
  return True

@multimethod(StepTile, EmptyTile, GrassTile, MountainTile,
                                                  rootto=True)
def can_enter(fro, to):
  return True

@SymmetricTravel(MountainTile)
def can_enter(fro, to):
  return True

"""
EmptyTile
SolidTile
EntranceTile
WaterTile
InteractTile
GrassTile
LedgeTile
MountainTile
StepTile
"""

@SymmetricTravel(LedgeTile, EmptyTile)
def can_enter(fro, to):
  print "sdfsdfdF"
  return False

@multimethod(SolidTile, WaterTile, GrassTile, StepTile, EntranceTile,
                                        MountainTile, LedgeTile, rootfrom=True)
def can_enter(fro, to):
  return False

