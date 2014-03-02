from utils import transform_points_for_pygame
import pygame
from shapely.geometry import Point
class Phone(pygame.sprite.Sprite, Point):
  movement_offset = 10

  def __init__(self, char, center, cells):
    pygame.sprite.Sprite.__init__(self)
    Point.__init__(self, center)

    # This is the unique name/address of the phone.
    self.id = char

    # These are all of the PCS cells in which this phone can be within.
    self.cells = cells

    # This is the geographic cell in which the phone is within. The center of
    #  this cell has a base station with which this phone can connect with
    #  to make calls, register its location, etc.
    self.num_writes = 0
    self.num_reads = 0
    self.PCS_cell = None
    for h in self.cells:
      if h.contains(self):
        self.PCS_cell = h
        h.register(self)

    # These member variables are required for this Phone class to be a
    #  sprite.
    self.image = pygame.image.load("phone.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.center = transform_points_for_pygame([center])[0]

    # If the phone is moved, the offset vector will be updated. It is a
    #  direction vector.
    self.offset = (0,0)

    # The label is drawn on top of the sprite.
    label_font = pygame.font.SysFont("monospace", 15)
    self.label = label_font.render(char, True, (255, 255, 255))
    self.draw_text()


  # This function is called by the RenderGroup object with which this phone is
  #  a member of.
  def update(self):
    x, y = self.coords[0]
    center = (
      x + self.movement_offset*self.offset[0],
      y + self.movement_offset*self.offset[1]
    )
    self.rect.center = transform_points_for_pygame([center])[0]
    self._set_coords(center)
    self.offset = (0,0)


  def draw_text(self):
    x = self.label.get_width()
    y = self.label.get_height()
    self.image.blit(self.label, (x, y))


  def move_by(self, offset_vector):
    self.offset = offset_vector


  def has_moved_to_new_cell(self):
    if self.PCS_cell is None:
      for h in self.cells:
        if h.contains(self):
          print("{0} has moved".format(self.id))
          return True
      return False

    else:
      if self.PCS_cell.contains(self):
        return False
      else:
        print("{0} has moved".format(self.id))
        return True

  def update_location(self):
    # It is assumed that the phone has updated its location, which is one of
    #  the possible update scenarios:
    #  1. None -> Cell
    #  2. Cell -> Cell
    #  3. Cell -> None
    if self.PCS_cell is None:
      #  1. None -> Cell
      for h in self.cells:
        if h.contains(self):
          self.PCS_cell = h
          h.register(self)
          return

    else:
      #  2. Cell -> Cell
      #  3. Cell -> None
      old_cell = self.PCS_cell
      self.PCS_cell = None
      for h in self.cells:
        if h.contains(self):
          self.PCS_cell = h
          h.register(self)

      if self.PCS_cell is None:
        # The phone has roamed out of its coverage area, and thus should
        #  perform a dark area deregister.
        old_cell.dark_spot_deregister(self)


