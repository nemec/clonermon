def print_outline(screen, tile):
  for px in tile.mask.outline():
    screen.set_at(px, (255, 0, 0))
