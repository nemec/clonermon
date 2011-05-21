import pygame.locals

class Controls:
  class MetaControls(type):
    valid_controls = {
      "A": pygame.locals.K_z,
      "B": pygame.locals.K_x,
      "UP": pygame.locals.K_UP,
      "DOWN": pygame.locals.K_DOWN,
      "LEFT": pygame.locals.K_LEFT,
      "RIGHT": pygame.locals.K_RIGHT,
      "START": pygame.locals.K_RETURN,
      "SELECT": pygame.locals.K_BACKSPACE,
    }

    def __getattr__(self, key):
      return self.valid_controls.get(key, None)

    def key_list(self):
      return self.valid_controls.keys()

    def val_list(self):
      return self.valid_controls.values()

  __metaclass__ = MetaControls

print Controls.vals


