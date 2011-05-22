import gtk
import gobject
from collections import defaultdict

class PainterGrid(gtk.HBox):

  __gsignals__ = {
    "model-changed" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
  }

  def __init__(self, palette, selected_tile):
    gtk.HBox.__init__(self)
    self.mapsize = 50
    self.tablesize = (10, 9)
    self.origin = tuple(self.mapsize // 2 - x for x in self.tablesize)
    self.palette = palette
    self.selected_tile = selected_tile
    rows, columns = self.tablesize
    self.table = gtk.Table(rows, columns, homogeneous = True)
    self.model = defaultdict(dict) # x, y coordinate with tile position as val
    self.start_position = (self.origin[0] + 4, self.origin[1] + 4)
    self.start_overlay = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                                                16,16)
    self.start_overlay.fill(0xff0000ff)

    for x in xrange(rows-1, -1, -1):
      for y in xrange(columns-1, -1, -1):
        eb = gtk.EventBox()
        im = gtk.Image()
        im.set_from_pixbuf(self.selected_tile.get_pixbuf())
        eb.add(im)
        self.table.attach(eb, x, x+1, y, y+1, gtk.SHRINK|gtk.FILL, gtk.SHRINK|gtk.FILL)
        eb.connect("drag-data-received", self.palette_tile_dropped)
        eb.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
                          gtk.DEST_DEFAULT_HIGHLIGHT |
                          gtk.DEST_DEFAULT_DROP,
                          [("text/uri-list", 0, 0)], gtk.gdk.ACTION_COPY)
        eb.set_events(gtk.gdk.LEAVE_NOTIFY_MASK |
                      gtk.gdk.BUTTON_PRESS_MASK |
                      gtk.gdk.POINTER_MOTION_MASK)
        eb.connect("button-press-event", self.button_press_event, (x, y))
        eb.connect("enter-notify-event", self.motion_notify_event, (x, y))

    hadj = gtk.Adjustment(self.origin[0], 0, self.mapsize, 1, self.tablesize[0]//2, self.tablesize[0])
    vadj = gtk.Adjustment(self.origin[1], 0, self.mapsize, 1, self.tablesize[1]//2, self.tablesize[1])
    hadj.connect("value-changed", self.hscroll_value_changed)
    vadj.connect("value-changed", self.vscroll_value_changed)
    vscroll = gtk.VScrollbar(vadj)
    hscroll = gtk.HScrollbar(hadj)

    def table_scroll_event(table, event):
      if event.direction == gtk.gdk.SCROLL_UP:
        vadj.value = vadj.value - 1
      elif event.direction == gtk.gdk.SCROLL_DOWN:
        vadj.value = vadj.value + 1
    self.table.connect("scroll-event", table_scroll_event)

    scrollbox = gtk.VBox(False, 2)
    scrollbox.pack_start(self.table, False, False)
    scrollbox.pack_start(hscroll, False, False)
    self.pack_start(scrollbox, False, False)
    self.pack_start(vscroll, False, False)


  def hscroll_value_changed(self, adj):
    newval = int(adj.get_value())
    if newval != self.origin[0]:
      self.origin = (newval, self.origin[1])
      self.update_table()


  def vscroll_value_changed(self, adj):
    newval = int(adj.get_value())
    if newval != self.origin[1]:
      self.origin = (self.origin[0], newval)
      self.update_table()


  def update_table(self):
    it = iter(self.table.get_children())
    ox, oy = self.origin
    for x in xrange(self.tablesize[0]):
      for y in xrange(self.tablesize[1]):
        cell = it.next()
        src = self.model.get(ox+x, dict()).get(oy+y, None)
        if src:
          sx, sy = src
          pb = self.palette[sx][sy]

        else:
          pb = self.selected_tile.empty_pixbuf
        if (ox+x, oy+y) == self.start_position:
          pb = self.new_overlay_pixbuf(pb)
        self.paint_tile(cell, pixbuf = pb)


  def palette_tile_dropped(self, box, context, x, y, selection, info, time):
    position = map(int, selection.data.split("|"))
    self.paint_tile(box, position)
    if context.action == gtk.gdk.ACTION_COPY:
        context.finish(True, False, time)


  def button_press_event(self, widget, event, pos):
    if event.button == 1:
      self.paint_tile(widget, pos)
      gtk.gdk.pointer_ungrab()
    return True


  def motion_notify_event(self, widget, event, pos):
    x = event.x
    y = event.y
    state = event.state
    if state & gtk.gdk.BUTTON1_MASK:
      self.paint_tile(widget, pos)
    return True

  def new_overlay_pixbuf(self, pixbuf, overlay = None):
    if not overlay:
      overlay = self.start_overlay
    pixbuf = pixbuf.copy()
    overlay.composite(pixbuf, 0, 0, pixbuf.props.width,
               pixbuf.props.height, 0, 0, 1.0, 1.0, gtk.gdk.INTERP_HYPER, 127)
    return pixbuf

  def paint_tile(self, eventbox, position = None, pixbuf = None):
    if not pixbuf:
      pixbuf = self.selected_tile.get_pixbuf()
    if position:
      x = position[0] + self.origin[0]
      y = position[1] + self.origin[1]
      if (x, y) == self.start_position:
        pixbuf = self.new_overlay_pixbuf(pixbuf)
      if self.selected_tile.tileset_location is not None:
        self.model[x][y] = self.selected_tile.tileset_location
        self.emit('model-changed')
      else:
        if x in self.model:
          if y in self.model[x]:
            del self.model[x][y]
          if len(self.model[x]) == 0:
            del self.model[x]
    img = eventbox.get_children()[0]
    img.set_from_pixbuf(pixbuf)
    
