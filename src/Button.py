import pygame
from src.Vector import Vector
from pygame import Surface

class Button():
	def __init__(self, image: Surface, position: Vector, text_input: str, font_name: str, font_size: int, base_color: str, hovering_color: str):
		self.x_position = position.x
		self.y_position = position.y
		self.font = pygame.font.Font(font_name, font_size)
		self.image = pygame.transform.scale(image, (500, self.font.get_height()))
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_position, self.y_position))
		self.text_rect = self.text.get_rect(center=(self.x_position, self.y_position))

	def update(self, screen: Surface):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position: Vector):
		if position.x in range(self.rect.left, self.rect.right) and position.y in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position: Vector):
		if position.x in range(self.rect.left, self.rect.right) and position.y in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)