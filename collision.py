import pygame.sprite
from tile import *

def sprite_collision(next_tile, tile):
  if pygame.sprite.collide_rect(next_tile, tile):
    #print player.current_tile, tile
    curr_loc = None 
    targ_loc = None
    for ix, t in enumerate(tiletypes):
      if isinstance(next_tile, t):
        curr_loc = ix
      if isinstance(tile, t):
        targ_loc = ix
    return not can_enter[curr_loc][targ_loc]
  return False

tiletypes = [ #Empty,Solid,Entrance,Water,Interact,Grass,Ledge,Mountain,Step
# tiletypes[row][col]
    EmptyTile, 
    SolidTile, 
    EntranceTile, 
    WaterTile, 
    InteractTile,
    GrassTile, 
    LedgeTile, 
    MountainTile, 
    StepTile,
  ]

can_enter = [
    [True, False,True, False,True, True, True, False,True],
    [False,False,False,False,False,False,False,False,False],
    [False,False,False,False,False,False,False,False,False],
    [True, False,True, True, True, True, False,False,True],
    [True, False,True, True, True, True, True, False,True],
    [True, False,True, False,True, True, True, False,True],
    [True, False,False,False,True, True, False,False,False],
    [False,False,False,False,False,False,False,False,False],
    [True, False,True, False,True, True, False,False,True],
 ]

