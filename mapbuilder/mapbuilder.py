import gtk
from collections import defaultdict

import grid

class SelectedTile(gtk.EventBox):
  def __init__(self, tilesize):
    gtk.EventBox.__init__(self)
    self.image = gtk.Image()
    self.tileset_location = None
    self.empty_pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                                                tilesize, tilesize)
    self.empty_pixbuf.fill(0xffffffff)
    pixmap,mask = self.empty_pixbuf.render_pixmap_and_mask()
    cm = pixmap.get_colormap()
    red = cm.alloc_color('red')
    gc = pixmap.new_gc(foreground=red)
    t = tilesize-1
    pixmap.draw_line(gc,t,0,t,t)
    pixmap.draw_line(gc,0,t,t,t)
    self.empty_pixbuf = self.empty_pixbuf.get_from_drawable(pixmap, cm,
                                                          0, 0, 0, 0, -1, -1)
    self.image.set_from_pixbuf(self.empty_pixbuf)
    self.add(self.image)


  def set_image(self, pixbuf, tileset_location):
    self.tileset_location = tileset_location
    self.image.set_from_pixbuf(pixbuf)


  def get_pixbuf(self):
    return self.image.get_pixbuf()


  def set_empty(self):
    self.tileset_location = None
    self.image.set_from_pixbuf(self.empty_pixbuf)
  

class MapBuilder(gtk.Window):

  def __init__(self, tileset_file = None):
    gtk.Window.__init__(self)
    self.set_title("Map Builder")
    self.tilesize = 16
    self.tileset = None
    self.tiles = None
    self.save_file = None
    self.need_to_save = False

    self.tileset_file = tileset_file
    if tileset_file is not None:
      self.load_tileset(tileset_file)
    if (self.tileset is None or
        self.tileset.get_width() % self.tilesize != 0 or
        self.tileset.get_height() % self.tilesize != 0):
      raise ValueError("Please set tilesize to an integer divisible "
                        "by {0} and {1}".format(tileset.width(), tileset.height()))

    self.set_default_size(200, 220)
    self.connect("delete-event", self.ensure_quit)

    self.selected_tile = SelectedTile(self.tilesize)

    vbox = gtk.VBox(False, 2)

    menubar = self.build_menubar()

    controls = gtk.HBox(False, 2)
    ctrl = self.add_controls(controls)

    builder = gtk.HBox(False, 2)
    palette = self.build_tileset()
    self.paintgrid = grid.PainterGrid(self.tiles, self.selected_tile)
    def model_changed(grid, window):
      title = window.get_title()
      if not title.endswith(" *"):
        window.set_title(title + " *")
      window.need_to_save = True
    self.paintgrid.connect("model-changed", model_changed, self)

    builder.pack_start(palette, False, False)
    builder.pack_end(self.paintgrid, False, False)

    vbox.pack_start(menubar, False, False)
    vbox.pack_start(controls)
    vbox.pack_end(builder)
    self.add(vbox)


  def ensure_quit(self, *args):
    quit = True
    if self.need_to_save:
      buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                  gtk.STOCK_QUIT, gtk.RESPONSE_REJECT,
                  gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT)
      save_dialog = gtk.Dialog("Save?", self, gtk.DIALOG_MODAL, buttons=buttons)
      save_label = gtk.Label("Do you want to save?")
      save_dialog.vbox.pack_start(save_label, True, True)
      save_label.show()
      response = save_dialog.run()
      if response == gtk.RESPONSE_ACCEPT:
        self.save_map_to_file(None, True)
      elif response == gtk.RESPONSE_CANCEL:
        quit = False
      save_dialog.destroy()
    if quit:
      gtk.main_quit()
    return True
    

  def create_new_map(self, menuitem):
    self.save_file = None
    raise NotImplementedError


  def save_map_to_file(self, menuitem, pickfile = False):
    if self.need_to_save:      
      if pickfile or self.save_file is None:
        savebuttons = (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                       gtk.STOCK_SAVE,gtk.RESPONSE_OK)
        chooser = gtk.FileChooserDialog(title=None,
                                        action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=savebuttons)
        chooser.set_current_name("new_map.map")
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
          filename = chooser.get_filename()
          try:
            f = open(filename, 'w')
            tileset_name = self.tileset_file[:self.tileset_file.rfind(".")]
            w, h = (self.paintgrid.mapsize,)*2
            x, y = self.paintgrid.start_position
            f.write(", ".join([tileset_name, str(self.tilesize), str(w),
                                                      str(h), str(x), str(y)]))
            f.write("\n")
            for x in self.paintgrid.model:
              adj_x = x - self.paintgrid.start_position[0]
              for y in self.paintgrid.model[x]:
                adj_y = y - self.paintgrid.start_position[1]
                f.write("{0}, {1}, {2}, {3}\n".format(adj_x, adj_y,
                                                  *self.paintgrid.model[x][y]))
            f.close()
            title = self.get_title()
            if title.endswith(" *"):
              self.set_title(title[:-2])
            self.need_to_save = False
          except IOError as e:
            err_dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL, 
                            gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, str(e))
            err_dialog.run()
            err_dialog.destroy()
        chooser.destroy()


  def palette_tile_dragged(self, iconview, context, selection, info, time):
    model = iconview.get_model()
    selected = iconview.get_selected_items()

    tile_loc = model[selected[0]][0]
    selection.set(selection.target, 8, tile_loc)


  def crop_pixbuf(self, image, x, y, w, h):
    temp = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, image.get_has_alpha(), 8, w, h)
    image.copy_area(x, y, w, h, temp, 0, 0)
    return temp


  def set_mode(self, widget, mode):
    if mode == "paint":
      print "paint"
    elif mode == "erase":
      self.selected_tile.set_empty()
    else:
      print "Unknown mode: " + mode


  def load_tileset(self, filename):
    self.tileset = gtk.gdk.pixbuf_new_from_file(filename)

  def update_selected_tile(self, iconview):
    model = iconview.get_model()
    selected = iconview.get_selected_items()
    tile_loc = model[selected[0]][0]
    x, y = map(int, tile_loc.split("|"))
    self.selected_tile.set_image(self.tiles[x][y], (x, y))


  def build_menubar(self):
    mb = gtk.MenuBar()

    filem = gtk.MenuItem("_File")
    filemenu = gtk.Menu()
    filem.set_submenu(filemenu)

    agr = gtk.AccelGroup()
    self.add_accel_group(agr)

    newi = gtk.ImageMenuItem(gtk.STOCK_NEW, agr)
    key, mod = gtk.accelerator_parse("<Control>N")
    newi.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
    newi.connect("activate", self.create_new_map)
    filemenu.append(newi)

    openi = gtk.ImageMenuItem(gtk.STOCK_OPEN, agr)
    key, mod = gtk.accelerator_parse("<Control>O")
    openi.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
    filemenu.append(openi)

    savei = gtk.ImageMenuItem(gtk.STOCK_SAVE, agr)
    key, mod = gtk.accelerator_parse("<Control>S")
    savei.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
    savei.connect("activate", self.save_map_to_file)
    filemenu.append(savei)

    sep = gtk.SeparatorMenuItem()
    filemenu.append(sep)

    exit = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
    key, mod = gtk.accelerator_parse("<Control>Q")
    exit.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
    exit.connect("activate", self.ensure_quit)
    filemenu.append(exit)

    mb.append(filem)

    return mb

  def add_controls(self, box):
    paint_button = gtk.Button("Paint")
    paint_button.connect("clicked", self.set_mode, "paint")
    box.pack_start(paint_button, False, False)

    erase_button = gtk.Button("Eraser")
    erase_button.connect("clicked", self.set_mode, "erase")
    box.pack_start(erase_button, False, False)

    selected_tile_label = gtk.Label("Selected:")
    box.pack_start(selected_tile_label, False, False)
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                                                self.tilesize, self.tilesize)
    pixbuf.fill(0xffffffff)
    box.pack_start(self.selected_tile, False, False)
    

  def build_tileset(self):
    self.tiles = defaultdict(dict)

    tileset_model = gtk.ListStore(str, gtk.gdk.Pixbuf)
    for ix, x in enumerate(xrange(0, self.tileset.get_height(), self.tilesize)):
      for iy, y in enumerate(xrange(0, self.tileset.get_width(), self.tilesize)):
        pix = self.crop_pixbuf(self.tileset, y, x, self.tilesize, self.tilesize)
        self.tiles[ix][iy] = pix
        loc = "{0}|{1}".format(ix, iy)
        tileset_model.append((loc, pix))

    self.palette = gtk.IconView(tileset_model)
    self.palette.set_pixbuf_column(1)
    self.palette.set_columns(-1)
    self.palette.set_selection_mode(gtk.SELECTION_SINGLE)
    self.palette.set_margin(0)
    self.palette.set_column_spacing(0)
    self.palette.set_row_spacing(0)
    self.palette.set_item_padding(0)
    pad = lambda s: s + s / self.tilesize * 2
    self.palette.set_size_request(pad(self.tileset.get_width()),
                              pad(self.tileset.get_height()))

    self.palette.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [("text/uri-list", 0, 0)], gtk.gdk.ACTION_COPY)
    self.palette.connect("drag-data-get", self.palette_tile_dragged)

    self.palette.connect("selection-changed", self.update_selected_tile)
  
    return self.palette


m = MapBuilder("/home/dan/prg/py/clonermon/reduced_tileset.png")
m.show_all()
gtk.main()
