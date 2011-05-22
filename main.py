import os
import sys
import pygame
import pygame.sprite
from pygame.locals import *

import tile
import gamemap
import character
import collision
import constants
from spritesheet import spritesheet
from controls import Controls, ControlState

import debug

pygame.init()

def setup_event_queue():
  pygame.event.set_allowed(None)
  pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
  pygame.key.set_repeat(50, 50)

def build_map(game_map):
  #out = tile.Outside()
  #pebbles = lambda : out.get_tile("pebbles")
  #ledge = lambda : out.get_tile("l_ledge")
  #mount = lambda : out.get_tile("c_mountain")
  #for x in xrange(20):
  #  for y in xrange(4):
      
  #game_map.add(pebbles(), (0,0))
  #game_map.add(ledge(), (0,-1))
  #game_map.add(ledge(), (1, 0))
  game_map.background.load_from_file("tiny.map")
  

def main():
  tile_size = 16
  game_map = gamemap.Screen(tilesize = tile_size)
  setup_event_queue()

  ss = spritesheet("people_16.png", size=tile_size, pad=2)
  player = character.Player(*ss.images_pos([(1,7),(1,0),(1,1)]))
  player.set_animated(*ss.images_pos([(1,3),(1,2),(0,8)]))
  game_map.set_player(player)

  build_map(game_map)

  clock = pygame.time.Clock()

  moving = False
  move_count = 0
  move_dist = 2

  running = True
  while running:
    clock.tick(constants.TICKSPEED)

    if not moving:
      keys = [k for k, p in enumerate(pygame.key.get_pressed()) if k in
                Controls.val_list and p]
      # Prefers movement with lower scancode first
      if len(keys) > 0:
        if player.will_move(keys[0]):
          adj = game_map.get_adjacent_tile(player, player.direction)
          if adj is None or not pygame.sprite.spritecollideany(adj, game_map,
                                                      collision.sprite_collision):
            moving = True
            continue
          else:
            game_map.update() # Just update our direction

      for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == QUIT:
          running = False
          break
        elif event.type == KEYDOWN and not ControlState.down(event.key):
          ControlState.set_down(event.key)
          if event.key == Controls.A:
            print "A"
          elif event.key == Controls.B:
            print "B"
          elif event.key == Controls.START:
            print "Start"
          elif event.key == Controls.SELECT:
            print "Select"
          elif event.key in debug.keybindings:
            debug.keybindings[event.key]()
          else:
            ControlState.set_up(event.key)
          pygame.event.clear(KEYDOWN)
        elif event.type == KEYUP:
          ControlState.set_up(event.key)
        
    else:
      if move_count == player.rect.height:# Player height == width, either works
        # set our current tile
        til = pygame.sprite.spritecollide(player, game_map, False)
        if til:
          player.current_tile = til[0]
        player.animate(False)
        moving = False
        move_count = 0
      else:
        # Only start animating halfway through, makes movement seem more fluid
        if move_count > player.rect.height/2:
          player.animate(True)

        cur_dist = move_dist

        # Make sure we don't move further than our height
        if cur_dist + move_count > player.rect.height:
          cur_dist = player.rect.height - move_count

        move_count+=cur_dist
        game_map.update(increment=cur_dist, direction=player.direction)
        
      pygame.event.clear(KEYDOWN)

    game_map.draw()
    pygame.display.update()

  print "Exiting..."
  pygame.quit()

if __name__ == "__main__": main()
