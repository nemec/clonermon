import pygame
from pygame.locals import *
import os, sys
from spritesheet import spritesheet
from controls import Controls
import GameMap
import tile
import pygame.sprite
import character
import collision

import debug

pygame.init()

def setup_event_queue():
  pygame.event.set_allowed(None)
  pygame.event.set_allowed([QUIT])
  pygame.key.set_repeat(50, 50)

def main():
  screen = pygame.display.set_mode((160,144))
  setup_event_queue()
  out = tile.Outside()
  background = pygame.Surface(screen.get_size())
  game_map = GameMap.Map()
  pebbles = out.get_tile("pebbles")
  ledge = out.get_tile("ledge")
  ledge.rect = ledge.rect.move((0,16))
  game_map.add(pebbles)
  game_map.add(ledge)
  ss = spritesheet("people_16.png", pad=2)
  player = character.Player(pebbles, *ss.images_pos([(1,7),(1,0),(1,1)]))
  player.set_animated(*ss.images_pos([(1,3),(1,2),(0,8)]))
  player.rect = player.rect.move(16*4, 16*4)
  playersprite = pygame.sprite.RenderPlain(player)

  background.fill((0,255,0))
  screen.blit(background, (0,0))

  clock = pygame.time.Clock()

  #screen.blit(*pebbles.get_blit())
  #debug.print_outline(screen, pebbles)
  moving = False
  move_count = 0
  move_dist = 2

  running = True
  while running:
    clock.tick(30)
    if not moving:
      move_screen = False
      keys = [k for k, p in enumerate(pygame.key.get_pressed()) if k in
                Controls.val_list() and p]
      # Smoother movement, doesn't always work
      # Unfortunately, prefers movement with lower scancode first
      if len(keys) > 0 and player.move(keys[0]):
        moving = True
      if Controls.A in keys:
        print "A"
      elif Controls.B in keys:
        print "B"
      elif Controls.START in keys:
        print "Start"
      elif Controls.SELECT in keys:
        print "Select"
      for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == QUIT:
          running = False
          break
    # Smooths over the moving - not moving transition
    if moving:
      if move_count == player.rect.height: # Player height = width, either works
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
        if cur_dist + move_count > player.rect.height:
          cur_dist = player.rect.height - move_count
        move_count+=cur_dist
        game_map.update(increment=cur_dist, direction=player.direction)
        collide = pygame.sprite.spritecollideany(player, game_map,
                                                    collision.sprite_collision)
        # Reverse the move
        if collide:
          game_map.update(increment=-cur_dist, direction=player.direction)
      pygame.event.clear(KEYDOWN)

    screen.blit(background, (0,0))
    playersprite.update(game_map)
    game_map.draw(screen)
    playersprite.draw(screen)
    pygame.display.update()

  print "Exiting..."
  pygame.quit()

if __name__ == "__main__": main()
