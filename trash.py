#old dialogue box script
class DialogueBox(pygame.sprite.Sprite):
    def __init__(self, text, game, follow):
        self.game = game
        self._layer = TOP_LAYER
        self.groups = self.game.all_sprites, self.game.dbox
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = self.game.player.rect.x - 350
        self.y = self.game.player.rect.y + 200
        self.width = 500
        self.height = 200

        self.follow = follow

        self.image = self.game.dialogue_box
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.font = pygame.font.Font("pixel_font.ttf", 20)
        self.content = text
        
        self.fg = BLACK
        
        self.game.player.freezed = True
        for e in self.game.enemies:
            e.freezed = True

        self.text = self.font.render(self.content, False, self.fg)
        self.text_rect = self.text.get_rect(topleft=(55, 45))
        
        self.image.blit(self.text, self.text_rect)

    def update(self):
        self.skip()
        if self.follow:
            self.follow_player()
    
    def follow_player(self):
        self.rect.x += self.game.player.last_x_shifting
        self.rect.y += self.game.player.last_y_shifting

    def skip(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game.player.freezed = False
            for e in self.game.enemies:
                e.freezed = False
            self.text = self.font.render("1111111111111111111111111111111111111111", False, self.fg)
            self.image.blit(self.text, self.text_rect)
            self.kill()