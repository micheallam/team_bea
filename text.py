import pygame

class text(object):
	def __init__(self, text, fontsize, rectcenter, font='Sysfont', color = (255, 255, 255)):
    self.font = pygame.font.SysFont(None, fontsize)
    self.text = self.font.render(text, False, textcolor)
    self.rect = self.text.get_rect(center=rectcenter)
    self.y_offset = 0
    
    def update(self, main):
        self.rect.y -= 1
        self.y_offset -= 1
        
        if self.y_offset == -100:
            main.get_map().remove_text(self)
    
    def render(self, main):
        main.screen.blit(self.text, self.rect)
        
    def render_in_game(self, main):
        main.screen.blit(self.text, core.get_map().get_camera().apply(self)