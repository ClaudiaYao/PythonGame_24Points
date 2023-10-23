import math
import pygame
from pgzero.actor import POS_TOPLEFT, ANCHOR_CENTER
from pgzhelper import Actor
from pgzero import game, loaders

class Exp_operator(Actor):
  def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
    self.first_operand = None
    self.second_operand = None
    super().__init__(image, pos, anchor, **kwargs)

  def get_first_position(self):
    return (self.x + self.width // 4, self.y + self.height // 2)

  def get_second_position(self):
    return (self.x + self.width // 8 * 5, self.y + self.height // 5)

  def is_first_operand(self, actor):
    print("first position check. first position : actor ->", self.get_first_position(), actor.x + actor.width // 2,
          actor.y + actor.height // 2)
    # if self.first_operand is None:
    dx = actor.x + actor.width // 2 - self.get_first_position()[0]
    dy = actor.y + actor.height // 2 - self.get_first_position()[1]
    print(math.sqrt(dx**2 + dy**2))
    return math.sqrt(dx**2 + dy**2) < 60

  def is_second_operand(self, actor):
    print("second position check. second position : actor ->", self.get_second_position(), actor.x + actor.width // 2,
          actor.y + actor.height // 2)
    # if self.second_operand is None:
    dx = actor.x + actor.width // 2 - self.get_second_position()[0]
    dy = actor.y + actor.height // 2 - self.get_second_position()[1]
    return math.sqrt(dx**2 + dy**2) < 50

  # def move(self, destination_pos):
  #   self.pos = destination_pos[0] - self.width // 2, destination_pos[1] - self.height//2
  #   if self.first_operand is not None:
  #     self.first_operand.pos = self.get_first_position()
  #
  #   if self.second_operand is not None:
  #     self.second_operand.pos = self.get_second_position()


class Root_operator(Actor):
  def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
    self.first_operand = None
    self.second_operand = None
    super().__init__(image, pos, anchor, **kwargs)

  def get_first_position(self):
    return (self.x + self.width // 5, self.y + self.height // 5)

  def get_second_position(self):
    return (self.x + self.width // 3 * 2, self.y + self.height // 2)

  def is_first_operand(self, actor):
    print("first position check. first position : actor ->", self.get_first_position(), actor.x + actor.width // 2,
          actor.y + actor.height // 2)
    # if self.first_operand is None:
    dx = actor.x + actor.width // 2 - self.get_first_position()[0]
    dy = actor.y + actor.height // 2 - self.get_first_position()[1]
    print(math.sqrt(dx ** 2 + dy ** 2))
    return math.sqrt(dx ** 2 + dy ** 2) < 60

  def is_second_operand(self, actor):
    print("second position check. second position : actor ->", self.get_second_position(), actor.x + actor.width // 2,
          actor.y + actor.height // 2)
    # if self.second_operand is None:
    dx = actor.x + actor.width // 2 - self.get_second_position()[0]
    dy = actor.y + actor.height // 2 - self.get_second_position()[1]
    return math.sqrt(dx ** 2 + dy ** 2) < 50

  # def move(self, destination_pos):
  #   self.pos = destination_pos[0] - self.width // 2, destination_pos[1] - self.height // 2
  #   if self.first_operand is not None:
  #     self.first_operand.pos = self.get_first_position()
  #
  #   if self.second_operand is not None:
  #     self.second_operand.pos = self.get_second_position()