# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame
import utils

class spritesheet(object):
  def __init__(self, filename, size=16, pad = 0):
    self.padding = pad
    self.size = size
    try:
      self.sheet = pygame.image.load(filename).convert_alpha()
    except pygame.error, message:
      print 'Unable to load spritesheet image:', filename
      raise SystemExit, message

  # Load a specific image from a specific rectangle
  def image_at(self, rectangle, colorkey = None):
    "Loads image from x,y,x+offset,y+offset"
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size)
    image.fill(utils.transparent_rgb)
    image.blit(self.sheet, (0, 0), rect)
    if colorkey is not None:
      if colorkey is -1:
        colorkey = image.get_at((0,0))
      image.set_colorkey(colorkey, pygame.RLEACCEL)
    else:
      image.set_colorkey(utils.transparent_rgb, pygame.RLEACCEL)
    return image

  # Load a whole bunch of images and return them as a list
  def images_at(self, rects, colorkey = None):
    "Loads multiple images, supply a list of coordinates" 
    return [self.image_at(rect, colorkey) for rect in rects]

  # Load a whole strip of images
  def load_strip(self, rect, image_count, colorkey = None):
    "Loads a strip of images and returns them as a list"
    tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
            for x in range(image_count)]
    return self.images_at(tups, colorkey)

  def image_pos(self, pos, colorkey = None):
    x = pos[0]*self.size + self.padding*pos[0]
    y = pos[1]*self.size + self.padding*pos[1]
    return self.image_at((x, y, self.size, self.size), colorkey)

  def images_pos(self, positions, colorkey = None):
    return [self.image_pos(pos, colorkey) for pos in positions]

if __name__ == "__main__":
  ss = spritesheet('pokemonrgb_various_sheet.png')
  # Sprite is 16x16 pixels at location 0,0 in the file...
  image = ss.image_at((0,0))
  # Load two images into an array, their transparent bit is (255, 255, 255)
  #allSprites = ss.images_at(((0, 0, 16, 16),(17, 0, 16,16)), colorkey=(255, 255, 255))
