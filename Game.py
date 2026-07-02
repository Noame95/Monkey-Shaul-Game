import math
import os
import random
import pygame
import pygame.time



class Screen:
    def __init__(self):
        self.WIDTH = pygame.display.Info().current_w
        self.HEIGHT = pygame.display.Info().current_h
        self.FPS = 60
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.BACKGROUND = pygame.image.load(os.path.join("Assets", "jungle.jpg"))

        self.WHITE = (255, 255, 255)
        self.BROWN = (156, 102, 31)
        self.YELLOW = (227, 207, 87)

        self.FONT = pygame.font.SysFont("comic sans", self.WIDTH // 20)


class Monke:

    def __init__(self):
        self.monke_x = 1000
        self.monke_y = 600
        self.MONKE_SPEED = 7
        self.MONKE_HEIGHT = 100
        self.MONKE_WIDTH = 100
        self.MONKE_IMAGE = pygame.image.load(os.path.join("Assets", "monke.png"))
        self.state = pygame.transform.scale(self.MONKE_IMAGE, (self.MONKE_WIDTH, self.MONKE_HEIGHT))

        self.MONKE_SAD_IMAGE = pygame.image.load(os.path.join("Assets", "monke_sad.png"))
        self.MONKE_EARS_IMAGE = pygame.image.load(os.path.join("Assets", "monke_lightning.png"))
        self.MONKE_EYES_IMAGE = pygame.image.load(os.path.join("Assets", "monke_stone.png"))
        self.MONKE_MOUTH_IMAGE = pygame.image.load(os.path.join("Assets", "monke_shatavari.png"))

        self.MONKE_SCREAM = os.path.join("Assets", "monke_sound.wav")
        self.MONKE_SCREAM = pygame.mixer.Sound(self.MONKE_SCREAM)
        self.MONKE_EATS = os.path.join("Assets", "monke_eats.wav")
        self.MONKE_EATS = pygame.mixer.Sound(self.MONKE_EATS)
        self.MONKE_LIGHTNING = os.path.join("Assets", "monke_lightning.wav")
        self.MONKE_LIGHTNING = pygame.mixer.Sound(self.MONKE_LIGHTNING)
        self.MONKE_SHATAVARI = os.path.join("Assets", "monke_shatavari.wav")
        self.MONKE_SHATAVARI = pygame.mixer.Sound(self.MONKE_SHATAVARI)
        self.MONKE_STONE = os.path.join("Assets", "monke_stone_hit.wav")
        self.MONKE_STONE = pygame.mixer.Sound(self.MONKE_STONE)

        self.HEART_IMAGE = pygame.image.load(os.path.join("Assets", "heart.png"))
        self.HEART = pygame.transform.scale(self.HEART_IMAGE, (50, 50))

        self.hearts = [self.HEART, self.HEART, self.HEART, self.HEART]

    def movement_place(self, k, dis):
        if k[pygame.K_UP] and self.monke_y - self.MONKE_SPEED > 0:
            self.monke_y -= self.MONKE_SPEED
        if k[pygame.K_DOWN] and self.monke_y + self.MONKE_SPEED + self.MONKE_HEIGHT < dis.HEIGHT:
            self.monke_y += self.MONKE_SPEED
        if k[pygame.K_LEFT] and self.monke_x - self.MONKE_SPEED > 0:
            self.monke_x -= self.MONKE_SPEED
        if k[pygame.K_RIGHT] and self.monke_x + self.MONKE_SPEED + self.MONKE_WIDTH < dis.WIDTH:
            self.monke_x += self.MONKE_SPEED

        return [self.monke_x, self.monke_y]


class Object:
    def __init__(self, image, dis):
        self.image = image
        self.state = pygame.transform.scale(image, (50, 50))
        self.objects_spacing = 100
        self.x = random.randint(dis.WIDTH // 8, int(dis.WIDTH // 1.25))
        self.x = self.x - self.x % self.objects_spacing
        self.y = 0
        self.falling = 5

    def fall(self):
        self.y += self.falling

    def out(self, dis):
        if self.y >= dis.HEIGHT:
            return True
        return False

    def change_pos(self, dis):
        self.x = random.randint(int(dis.WIDTH // 8), int(dis.WIDTH // 1.25))
        self.y = 0

    def check_pos(self, list_of_obj, dis):
        for other_obj in list_of_obj:
            if other_obj != self:
                distance = math.sqrt((self.x - other_obj.x) ** 2)
                if distance < self.objects_spacing and self.y == other_obj.y:
                    self.change_pos(dis)
                    self.check_pos(list_of_obj, dis)

    def check_valid_pos(self, dis):
        if self.x > dis.WIDTH // 1.25 or self.x < dis.WIDTH // 8:
            self.change_pos(dis)
            self.check_valid_pos(dis)


class Game:
    def __init__(self):
        self.shaul = Monke()
        self.screen = Screen()
        self.menu = Menu(self.screen)

        self.clock = pygame.time.Clock()
        self.apply_buttons = True
        self.run = True
        self.loading = False

        self.SEN1 = self.screen.FONT.render("SAY HELLO TO SHAUL!", True, self.screen.YELLOW)
        self.SEN2 = self.screen.FONT.render("HMMM...SHAUL?", True, self.screen.YELLOW)
        self.SEN3 = self.screen.FONT.render("OH! THERE HE IS!", True, self.screen.YELLOW)
        self.SEN4 = self.screen.FONT.render("HELP SHAUL CATCH THE BANANAS!", True, self.screen.YELLOW)
        self.SEN5 = self.screen.FONT.render("(move with the arrows)", True, self.screen.YELLOW)
        self.LIST_OF_SEN = [self.SEN1, self.SEN2, self.SEN3, self.SEN4, self.SEN5]

        self.BANANA = Object(pygame.image.load(os.path.join("Assets", "banana.png")), self.screen)
        self.LIGHTNING = Object(pygame.image.load(os.path.join("Assets", "lightning.png")), self.screen)
        self.STONE = Object(pygame.image.load(os.path.join("Assets", "stone.png")), self.screen)
        self.SHATAVARI = Object(pygame.image.load(os.path.join("Assets", "shatavari.png")), self.screen)
        self.OBJECTS = [self.STONE, self.BANANA, self.LIGHTNING, self.SHATAVARI]
        self.falling_objects = []
        self.score = 0

        self.GAME_OVER = pygame.transform.scale(self.screen.FONT.render("GAME OVER!", True, self.screen.YELLOW),
                                                (self.menu.TITLE.get_width(), self.menu.TITLE.get_height()))

    def show_update_monke_move(self):
        keybind = pygame.key.get_pressed()
        move = self.shaul.movement_place(keybind, self.screen)
        monke_x, monke_y = move[0], move[1]
        self.screen.display.blit(self.screen.BACKGROUND, (0, 0))
        self.screen.display.blit(self.shaul.state, (monke_x, monke_y))

    def show_stats(self):
        heart_x = 0
        for heart in self.shaul.hearts:
            self.screen.display.blit(heart, (heart_x, 0))
            heart_x += 55
        score_text = pygame.transform.scale(self.screen.FONT.render("SCORE: " + str(self.score), True,
                                                                    self.screen.YELLOW), (220, 150))
        self.screen.display.blit(score_text, (0, 100))

    def create_object(self):
        for OBJ in self.OBJECTS:
            OBJ.check_pos(self.OBJECTS, self.screen)
            self.screen.display.blit(OBJ.state, (OBJ.x, OBJ.y))
            OBJ.fall()
            self.falling_objects.append(OBJ)

    def check_object_fall(self):
        for obj in self.falling_objects:
            if obj.out(self.screen):
                self.falling_objects.remove(obj)
                obj.change_pos(self.screen)

    def check_hit(self):
        for obj in self.falling_objects:
            obj_rect = pygame.Rect(obj.x, obj.y, obj.state.get_width(), obj.state.get_height())
            monkey_rect = pygame.Rect(self.shaul.monke_x, self.shaul.monke_y, self.shaul.state.get_width(),
                                      self.shaul.state.get_height())
            if monkey_rect.colliderect(obj_rect):
                self.falling_objects.remove(obj)
                obj.change_pos(self.screen)
                if obj == self.BANANA:
                    self.score += 1
                    self.shaul.state = pygame.transform.scale(self.shaul.MONKE_IMAGE, (self.shaul.MONKE_WIDTH,
                                                                                       self.shaul.MONKE_HEIGHT))
                    self.shaul.MONKE_EATS.play(fade_ms=0)
                elif obj == self.STONE:
                    self.shaul.state = pygame.transform.scale(self.shaul.MONKE_EYES_IMAGE, (self.shaul.MONKE_WIDTH,
                                                                                            self.shaul.MONKE_HEIGHT))
                    self.shaul.hearts.pop()
                    self.shaul.MONKE_STONE.play(fade_ms=0)
                elif obj == self.SHATAVARI:
                    self.shaul.state = pygame.transform.scale(self.shaul.MONKE_MOUTH_IMAGE, (self.shaul.MONKE_WIDTH,
                                                                                             self.shaul.MONKE_HEIGHT))
                    self.shaul.hearts.pop()
                    self.shaul.MONKE_SHATAVARI.play(fade_ms=0)
                elif obj == self.LIGHTNING:
                    self.shaul.state = pygame.transform.scale(self.shaul.MONKE_EARS_IMAGE, (self.shaul.MONKE_WIDTH,
                                                                                            self.shaul.MONKE_HEIGHT))
                    self.shaul.hearts.pop()
                    self.shaul.MONKE_LIGHTNING.play(fade_ms=0)

    def loading_screen(self):
        self.screen.display.blit(self.screen.BACKGROUND, (0, 0))
        pygame.mixer.music.set_volume(0.25)
        for SEN in self.LIST_OF_SEN:
            sen = pygame.transform.scale(SEN, (700, 150))
            self.screen.display.blit(sen, (self.menu.TITLE_X - 250, self.menu.TITLE_Y))
            pygame.display.update()
            pygame.time.delay(4000)
            self.screen.display.blit(self.screen.BACKGROUND, (0, 0))
            if self.LIST_OF_SEN.index(SEN) > 0:
                self.screen.display.blit(self.shaul.state, (1000, 600))
        self.loading = False

    def lose(self):
        self.shaul.state = pygame.transform.scale(self.shaul.MONKE_SAD_IMAGE, (self.shaul.MONKE_WIDTH,
                                                                               self.shaul.MONKE_HEIGHT))
        self.show_stats()
        self.screen.display.blit(self.GAME_OVER, (self.menu.TITLE_X, self.menu.TITLE_Y))
        self.screen.display.blit(self.shaul.state, (self.shaul.monke_x, self.shaul.monke_y))

    def make_game_harder(self):
        for OBJ in self.OBJECTS:
            if self.score % 10 == 0 and self.score != 0 and OBJ.falling < 6:
                OBJ.falling += 0.10

    def main(self):
        self.menu.create_menu()
        self.menu.create_buttons()
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.apply_buttons:
                    self.menu.check_music()
                    if self.menu.check_buttons_play_and_quit() == False:
                        self.run = False
                    elif self.menu.check_buttons_play_and_quit() == True:
                        self.apply_buttons = False

            if self.apply_buttons == False:
                self.show_update_monke_move()
                self.show_stats()
                if len(self.shaul.hearts) > 0:
                    self.create_object()
                    self.check_object_fall()
                    self.check_hit()
                    self.show_stats()
                    self.make_game_harder()
                else:
                    self.lose()
                    self.shaul.MONKE_SCREAM.play(fade_ms=0)
                    pygame.display.update()
                    pygame.time.delay(4000)
                    self.run = False
            self.clock.tick(self.screen.FPS)
            pygame.display.update()
        pygame.quit()


class Button:
    def __init__(self, x, y, width, height, text, text_x, text_y, text_color, button_color):
        self.text_y = text_y
        self.text_x = text_x
        self.button_color = button_color
        self.text_color = text_color
        self.text = text
        self.height = height
        self.width = width
        self.y = y
        self.x = x

    def create_button(self, dis):
        button = pygame.Surface((self.width, self.height))
        button.fill(self.button_color)
        dis.display.blit(button, (self.x, self.y))
        dis.display.blit(self.text, (self.text_x, self.text_y))
        pygame.display.update()


class Menu:

    def __init__(self, dis):
        self.dis = dis
        self.music_on = True
        self.MUSIC = os.path.join("Assets", "music.wav")
        self.TITLE = self.dis.FONT.render("MONKE SHAUL", True, self.dis.YELLOW)
        self.TITLE_X = self.dis.WIDTH / 3.5 + 125
        self.TITLE_Y = self.dis.HEIGHT / 7
        self.MONKE_MENU_Y = self.TITLE_Y // 2
        self.MONKE_MENU = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "monke.png")), (50, 50))
        self.AMOUNT_OF_MONKE_MENU = 5
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_X = dis.WIDTH // 2 - self.BUTTON_WIDTH // 2
        self.BUTTON_Y = dis.HEIGHT // 2 - self.BUTTON_HEIGHT // 2
        self.BUTTON_SPACING = self.BUTTON_WIDTH / 10

        # The top of the play button
        self.BUTTON_PLAY_Y = self.BUTTON_Y
        # The top of the music button
        self.BUTTON_MUSIC_Y = self.BUTTON_PLAY_Y + self.BUTTON_HEIGHT + self.BUTTON_SPACING
        # The top of the quit button
        self.BUTTON_QUIT_Y = self.BUTTON_MUSIC_Y + self.BUTTON_HEIGHT + self.BUTTON_SPACING

        self.PLAY_TEXT = pygame.font.SysFont("comic sans", 30).render("Play", True, dis.YELLOW)
        self.MUSIC_TEXT = pygame.font.SysFont("comic sans", 30).render("Music", True, dis.YELLOW)
        self.QUIT_TEXT = pygame.font.SysFont("comic sans", 30).render("Quit", True, dis.YELLOW)

        self.TEXT_X = self.BUTTON_X + self.BUTTON_WIDTH // 2 - self.PLAY_TEXT.get_width() // 2
        self.PLAY_TEXT_Y = self.BUTTON_Y + self.BUTTON_HEIGHT // 2 - self.PLAY_TEXT.get_height() // 2
        self.MUSIC_TEXT_Y = self.BUTTON_Y + self.BUTTON_HEIGHT + self.BUTTON_SPACING + self.BUTTON_HEIGHT // 2 - self. \
            MUSIC_TEXT.get_height() // 2
        self.QUIT_TEXT_Y = self.MUSIC_TEXT_Y + self.BUTTON_HEIGHT + self.BUTTON_SPACING

        self.play_button = None
        self.music_button = None
        self.quit_button = None

    def create_buttons(self):
        self.play_button = Button(self.BUTTON_X, self.BUTTON_PLAY_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT,
                                  self.PLAY_TEXT, self.TEXT_X, self.PLAY_TEXT_Y,
                                  self.dis.YELLOW, self.dis.BROWN)
        self.music_button = Button(self.BUTTON_X, self.BUTTON_MUSIC_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT,
                                   self.MUSIC_TEXT, self.TEXT_X, self.MUSIC_TEXT_Y,
                                   self.dis.YELLOW, self.dis.BROWN)
        self.quit_button = Button(self.BUTTON_X, self.BUTTON_QUIT_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT,
                                  self.QUIT_TEXT, self.TEXT_X, self.QUIT_TEXT_Y,
                                  self.dis.YELLOW, self.dis.BROWN)

        self.play_button.create_button(self.dis)
        self.music_button.create_button(self.dis)
        self.quit_button.create_button(self.dis)

    def create_menu(self):
        self.dis.display.blit(self.dis.BACKGROUND, (0, 0))
        self.dis.display.blit(self.TITLE, (self.TITLE_X, self.TITLE_Y))
        monke_menu_x = self.TITLE_X
        n = self.AMOUNT_OF_MONKE_MENU
        while n != 0:
            self.dis.display.blit(self.MONKE_MENU, (monke_menu_x, self.MONKE_MENU_Y))
            monke_menu_x += 170
            n -= 1

        pygame.mixer.music.load(self.MUSIC)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def check_buttons_play_and_quit(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if self.BUTTON_X <= mouse_x <= self.BUTTON_X + self.BUTTON_WIDTH and self.BUTTON_Y <= mouse_y <= \
                self.BUTTON_PLAY_Y + self.BUTTON_HEIGHT:
            return True
        elif self.BUTTON_X <= mouse_x <= self.BUTTON_X + self.BUTTON_WIDTH and self.BUTTON_QUIT_Y <= mouse_y <= \
                self.BUTTON_QUIT_Y + self.BUTTON_HEIGHT:
            return False

    def check_music(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if self.BUTTON_X <= mouse_x <= self.BUTTON_X + self.BUTTON_WIDTH and self.BUTTON_MUSIC_Y <= mouse_y <= \
                self.BUTTON_MUSIC_Y + self.BUTTON_HEIGHT:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                return False
            else:
                pygame.mixer.music.play()
                return True


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    game = Game()
    game.main()
