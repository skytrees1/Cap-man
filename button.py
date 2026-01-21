import pygame as p

class Button:
    def __init__(self, x, y, width, height, text, image, hover_image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = p.image.load(image)
        self.image = p.transform.scale(self.image, (width, height))
        self.hover_image = None
        if hover_image:
            self.hover_image = p.image.load(hover_image)
            self.hover_image = p.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.is_hovered = False
    
    def draw(self, screen):
        if self.is_hovered and self.hover_image:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)

        font = p.font.Font(None, 50)
        if self.is_hovered and self.hover_image:
            text_surface = font.render(self.text, True, (0,0,0))
        else:
            text_surface = font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    
    def handle_event(self, event, pos=None):
        if pos is None:
            pos = p.mouse.get_pos()
            
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                p.event.post(p.event.Event(p.USEREVENT, button=self))