import pygame
import random
import sys



pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('sablon/music.mp3')
pygame.mixer.music.play(-1)

width, height = 600, 800
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (135, 206, 250)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

background_img = pygame.image.load('sablon/arkaplan.png')
background_img = pygame.transform.scale(background_img, (width, height))

bird_img = pygame.image.load('sablon/kus.jpg')
bird_img = pygame.transform.scale(bird_img, (25, 25))

bird_img.set_colorkey(white)

class Button:
    def __init__(self, x, y, radius, color, text):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        text_surf = self.font.render(self.text, True, black)
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        screen.blit(text_surf, text_rect)

    def check_click(self, pos):
        return (pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2 <= self.radius ** 2

class Pipe:
    def __init__(self):
        self.width = 70
        self.height = random.randint(150, height - 150)
        self.x = width
        self.gap = 150
        self.passed = False

    def draw(self):
        pygame.draw.rect(screen, green, [self.x, 0, self.width, self.height])
        pygame.draw.rect(screen, green, [self.x, self.height + self.gap, self.width, height - self.height - self.gap])

    def move(self):
        self.x -= 5

def oyunLoopu():
    oyun_bitti = False
    kus_y = height / 2
    kus_x = 50
    kus_hiz = 0
    yer_cekim = 0.5
    ziplama = -7
    aci = 0
    skor = 0
    ziplama_basili = False

    borular = [Pipe()]

    while not oyun_bitti:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ziplama_basili = True
            if event.type == pygame.MOUSEBUTTONUP:
                ziplama_basili = False

        aci = min(max(-30, (kus_hiz / 10) * 30), 30)

        if ziplama_basili:
            kus_hiz = ziplama
        else:
            kus_hiz += yer_cekim

        kus_y += kus_hiz

        screen.blit(background_img, (0, 0))

        for boru in borular:
            boru.move()
            boru.draw()
            if boru.x + boru.width < 0:
                borular.remove(boru)
                skor += 1
            if not boru.passed and boru.x < 100:
                boru.passed = True
                borular.append(Pipe())
            if (kus_y < boru.height or kus_y > boru.height + boru.gap) and boru.x < 100 + 25:
                oyun_bitti = True
            if boru.x + boru.width < 50 and not boru.passed:
                boru.passed = True

        donmus_kus = pygame.transform.rotate(bird_img, aci)
        kus_dikdortgeni = donmus_kus.get_rect(center=(kus_x, kus_y))
        screen.blit(donmus_kus, kus_dikdortgeni.topleft)

        font = pygame.font.Font(None, 36)
        skor_text = font.render(f'Skor: {skor}', True, black)
        screen.blit(skor_text, (10, 10))

        pygame.display.update()

        if len(borular) == 0:
            borular.append(Pipe())

        pygame.time.Clock().tick(45)

    yeniden_baslat_button = Button(width // 2 - 100, height // 2 + 50, 50, (200, 200, 255), 'Devam')
    cikis_button = Button(width // 2 + 100, height // 2 + 50, 50, (255, 0, 0), 'Çıkış')

    while oyun_bitti:
        screen.blit(background_img, (0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('OYUN BİTTİ', True, black)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2 - 100))

        yeniden_baslat_button.draw()
        cikis_button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if yeniden_baslat_button.check_click(pos):
                    oyunLoopu()
                if cikis_button.check_click(pos):
                    pygame.quit()
                    sys.exit()
oyunLoopu()
