import pygame.locals

import collision
import constants
from controls import Controls

keybindings = {}

Controls.valid_controls["speedup"] = pygame.locals.K_SPACE
def _speedup():
  old = False
  tmp = None
  new = constants.TICKSPEED * 2

  while True:
    on  = yield old
    if on is not None:
      if on and tmp is None:
        print "Speeding up"
        tmp = constants.TICKSPEED
        constants.TICKSPEED = new
      elif not on and tmp is not None:
        print "Slowing down"
        constants.TICKSPEED = tmp
        tmp = None
      old = on
speedup = _speedup().send
speedup(None)

def speedup_toggle():
  if speedup(None):
    speedup(False)
  else:
    speedup(True)
keybindings[pygame.locals.K_SPACE] = speedup_toggle
      

Controls.valid_controls["walk_through_walls"] = pygame.locals.K_w
def _walk_through_walls():
  fn = None
  old = False

  def fake_collision(*args, **kwargs):
    return False

  while True:
    on = yield old
    if on is not None:
      if on and fn is None:
        print "Enabling walk through walls cheat."
        fn = collision.sprite_collision
        collision.sprite_collision = fake_collision
      elif not on and fn is not None:
        print "Disabling walk through walls cheat."
        collision.sprite_collision = fn
        fn = None
      old = on
walk_through_walls = _walk_through_walls().send
walk_through_walls(None)

def walk_through_walls_toggle():
  if walk_through_walls(None):
    walk_through_walls(False)
  else:
    walk_through_walls(True)
keybindings[pygame.locals.K_w] = walk_through_walls_toggle

if __name__ == "__main__":

  walk_through_walls(True)
  print walk_through_walls(None) == True
  walk_through_walls(True)
  walk_through_walls(False)
  print walk_through_walls(None) == False
  walk_through_walls(False)
  walk_through_walls(True)
