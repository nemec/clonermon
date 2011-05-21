from pygame.locals import *

transparent_rgb = (255, 0, 255)

def get_new_position(pos, direction, dist=1):
  if direction == K_UP:
    return (pos[0], pos[1]-dist)
  elif direction == K_DOWN:
    return (pos[0], pos[1]+dist)
  elif direction == K_LEFT:
    return (pos[0]-dist, pos[1])
  elif direction == K_RIGHT:
    return (pos[0]+dist, pos[1])
  return None

