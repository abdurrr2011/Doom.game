import pygame, sys, math, random
from sound import bg_music
from sound import shoot_sound, play_shoot,stop_bg_music,game_music,load_end_sounds, play_win, play_lose
  # ДЫБЫСТЫ ЖҮКТЕЙМІЗ!


# ---------------------- INIT ----------------------
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
W,H = screen.get_size()
clock = pygame.time.Clock()
FPS = 55
bg_music()
shoot_sound()
load_end_sounds()
# ---------------------- COLORS ----------------------
WHITE = (240,240,240)
RED = (200,40,40)
GREEN = (60,200,80)
YELLOW = (230,200,40)
DARK_RED = (80,10,10)
MARS_RED = (40,0,20)
MARS_ORANGE = (100,20,0)
BLACK = (0,0,0)

# ---------------------- FLOOR TEXTURE ----------------------
floor_tex = pygame.Surface((64,64))
floor_tex.fill((30,0,10))
for i in range(0,64,4):
    pygame.draw.line(floor_tex,(60,10,10),(i,0),(i,64),1)
    pygame.draw.line(floor_tex,(60,10,10),(0,i),(64,i),1)
for _ in range(20):
    x = random.randint(0,63)
    y = random.randint(0,63)
    w = random.randint(2,5)
    h = random.randint(2,5)
    pygame.draw.ellipse(floor_tex,(80,20,20),(x,y,w,h))

# ---------------------- WALL TEXTURE ----------------------
wall_tex = pygame.Surface((64,64))
wall_tex.fill((90,15,15))
for i in range(0,64,8):
    pygame.draw.rect(wall_tex,(150,40,40),(i,i,8,8))
for _ in range(15):
    x1 = random.randint(0,64)
    y1 = random.randint(0,64)
    x2 = random.randint(0,64)
    y2 = random.randint(0,64)
    pygame.draw.line(wall_tex,(200,50,50),(x1,y1),(x2,y2),1)

# ---------------------- SPRITES ----------------------
def make_player_sprite(scale=7):
    frames = []
    for i in range(3):
        s = pygame.Surface((8,8), pygame.SRCALPHA)
        # Негізгі дене – ашық қызыл
        pygame.draw.rect(s, (220,50,50), (2,2,4,5))
        # Қолдар – қара
        pygame.draw.rect(s,(30,30,30),(1,3,1,2))
        pygame.draw.rect(s,(30,30,30),(6,3,1,2))
        # Көздер – сары
        pygame.draw.rect(s,(255,255,0),(3,2,2,1))
        # Кішкене қозғалыс эффекті
        offset = i - 1
        pygame.draw.rect(s,(220,50,50),(2,2+offset,4,5))
        frames.append(pygame.transform.scale(s,(8*scale,8*scale)))
    return frames

# Ойыншы спрайтын жаңарту
PLAYER_SPR = make_player_sprite(7)







def make_imp_sprite(scale=5):
    frames = []
    for i in range(2):
        s = pygame.Surface((8,8), pygame.SRCALPHA)
        # Негізгі дене – қызыл-қоңыр
        pygame.draw.rect(s,(180,40,40),(2,2,4,5))
        # Қолдар
        pygame.draw.rect(s,(100,30,30),(1,3+i,1,2))
        pygame.draw.rect(s,(100,30,30),(6,3+i,1,2))
        # Көздер (жарық)
        pygame.draw.rect(s,(255,255,0),(3,2,2,1))
        frames.append(pygame.transform.scale(s,(8*scale,8*scale)))
    return frames



def make_caco_sprite(scale=7):
    frames = []
    for i in range(3):
        s = pygame.Surface((10,10), pygame.SRCALPHA)
        # Негізгі дене
        pygame.draw.ellipse(s,(180,30,0),(0,2,10,6))
        # Қозғалыс үшін қызыл дақтар
        pygame.draw.circle(s,(255,50,50),(3,5-i),2)
        pygame.draw.circle(s,(255,50,50),(7,5+i),2)
        frames.append(pygame.transform.scale(s,(10*scale,10*scale)))
    return frames



def make_final_demon_sprite(scale=20):
    frames = []
    for i in range(4):
        s = pygame.Surface((12,12), pygame.SRCALPHA)
        # Негізгі дене
        pygame.draw.circle(s,(150,0,0),(6,6),6)
        # Көздері / жарық
        pygame.draw.circle(s,(255,180,0),(4,4-i),3)
        pygame.draw.circle(s,(255,180,0),(8,4+i),3)
        # Қара пентагон тәрізді құлақ / бұрыш
        pygame.draw.polygon(s,(100,0,0),[(6,0+i),(10,6),(6,12-i),(2,6)])
        frames.append(pygame.transform.scale(s,(12*scale,12*scale)))
    return frames



PLAYER_SPR = make_player_sprite(7)
IMP_SPR = make_imp_sprite(5)
CACO_SPR = make_caco_sprite(7)
FINAL_SPR = make_final_demon_sprite(20)

# ---------------------- PLAYER ARROW ----------------------
def draw_player_arrow(surface, x, y, angle):
    size = 18
    p1 = (x + math.cos(angle) * size, y + math.sin(angle) * size)
    p2 = (x + math.cos(angle + 2.5) * 10, y + math.sin(angle + 2.5) * 10)
    p3 = (x + math.cos(angle - 2.5) * 10, y + math.sin(angle - 2.5) * 10)
    pygame.draw.polygon(surface, WHITE, [p1, p2, p3])

# ---------------------- ENTITIES ----------------------
class Player:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.hp=150; self.max_hp=150
        self.speed=3.6
        self.radius=16
        self.sprite=PLAYER_SPR
        self.frame_index=0
        self.frame_timer=0
        self.shotgun_ammo=8
        self.score=0

    def update_animation(self):
        self.frame_timer += 1
        if self.frame_timer % 10 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.sprite)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(self.radius, min(W - self.radius, self.x))
        self.y = max(self.radius, min(H - self.radius, self.y))

    def draw(self, surf,current_wave):
        # ---------- Shadow ----------
        pygame.draw.circle(surf, (0, 0, 0, 50), (int(self.x), int(self.y + 8)), self.radius)
        r = self.sprite[self.frame_index].get_rect(center=(int(self.x), int(self.y)))
        surf.blit(self.sprite[self.frame_index], r)

        # ---------- HUD BOX ----------
        hud_x, hud_y = 20, 20
        hud_w, hud_h = 280, 80
        pygame.draw.rect(surf, (30, 30, 30), (hud_x, hud_y, hud_w, hud_h), border_radius=8)  # фон
        pygame.draw.rect(surf, (200, 200, 200), (hud_x, hud_y, hud_w, hud_h), 2, border_radius=8)  # контур

        # ---------- Level + Difficulty ----------
        wave_names = ["First wave", "Second wave", "Third wave", "FINAL"]
        hud_font = pygame.font.SysFont("Courier New", 22, bold=True)
        level_txt = hud_font.render(f'{wave_names[current_wave]}', True, WHITE)
        surf.blit(level_txt, (hud_x + 10, hud_y + 10))

        # ---------- Ammo ----------
        ammo_txt = pygame.font.SysFont('Impact', 22).render(f'Ammo: {self.shotgun_ammo}', True, WHITE)
        surf.blit(ammo_txt, (hud_x + 10, hud_y + 40))

        # ---------- HP (HUD астында бөлек) ----------
        hp_bar_w = 180
        hp_bar_h = 18
        hp_x = hud_x  # HUD-тің сол жағына шығарамыз
        hp_y = hud_y + hud_h + 10  # HUD-тің астында 10 пиксель қашықтық

        # HP фон
        pygame.draw.rect(surf, (50, 50, 50), (hp_x, hp_y, hp_bar_w, hp_bar_h), border_radius=6)
        # HP градиент
        hp_ratio = self.hp / self.max_hp
        if hp_ratio > 0.5:
            color = (50, 220, 50)  # жасыл
        elif hp_ratio > 0.2:
            color = (220, 180, 20)  # сары
        else:
            color = (220, 50, 50)  # қызыл
        pygame.draw.rect(surf, color, (hp_x, hp_y, int(hp_bar_w * hp_ratio), hp_bar_h), border_radius=6)
        # HP контур
        pygame.draw.rect(surf, WHITE, (hp_x, hp_y, hp_bar_w, hp_bar_h), 2, border_radius=6)


class Enemy:
    def __init__(self,x,y,hp,speed,radius,sprite):
        self.x,self.y=x,y
        self.hp=hp; self.max_hp=hp
        self.speed=speed
        self.radius=radius
        self.sprite=sprite
        self.frame_index=0
        self.frame_timer=0

    def update_animation(self):
        self.frame_timer += 1
        if self.frame_timer % 15 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.sprite)

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self,surf):
        pygame.draw.circle(surf,(0,0,0,50),(int(self.x),int(self.y+6)),self.radius)
        r=self.sprite[self.frame_index].get_rect(center=(int(self.x),int(self.y)))
        surf.blit(self.sprite[self.frame_index],r)
        pygame.draw.rect(surf,RED,(self.x-22,self.y-28,44,6))
        pygame.draw.rect(surf,GREEN,(self.x-22,self.y-28,int(44*(self.hp/self.max_hp)),6))

class Bullet:
    def __init__(self,x,y,angle,speed=14,dmg=22):
        self.x=x; self.y=y
        self.dx=math.cos(angle)*speed
        self.dy=math.sin(angle)*speed
        self.dmg=dmg; self.radius=4

    def update(self):
        self.x+=self.dx; self.y+=self.dy

    def draw(self,surf):
        pygame.draw.circle(surf,YELLOW,(int(self.x),int(self.y)),self.radius)

# ---------------------- LEVELS ----------------------
levels = ["Красная пыль","Потерянный отсек","Усилительный модуль","Гнездо Какодемона","Ядерная Комната"]
current_level=0

# ---------------------- FOG SYSTEM ----------------------
fog_particles = []

def generate_fog_particles(num):
    particles = []
    for _ in range(num):
        x = random.randint(0, W)
        y = random.randint(0, H)
        base_size = random.randint(100, 260)
        speed = random.uniform(0.1, 0.4)
        alpha = random.randint(35, 70)
        pulse_speed = random.uniform(0.003, 0.008)
        pulse_phase = random.uniform(0, 3.14)
        fog_surface = pygame.Surface((base_size, base_size), pygame.SRCALPHA)
        pygame.draw.circle(fog_surface, (60, 70, 120, alpha), (base_size//2, base_size//2), base_size//2)
        particles.append([fog_surface, x, y, speed, base_size, pulse_speed, pulse_phase])
    return particles

def draw_fog(screen):
    global fog_particles
    if len(fog_particles) < 12:
        fog_particles = generate_fog_particles(12)
    for i, data in enumerate(fog_particles):
        fog, x, y, speed, base_size, pulse_speed, pulse_phase = data
        pulse = (math.sin(pulse_phase)+1)*0.5
        pulse_phase += pulse_speed
        size = int(base_size + pulse*40)
        fog_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        alpha = 45 + int(pulse*30)
        pygame.draw.circle(fog_surface,(60,70,120,alpha),(size//2,size//2),size//2)
        x += speed
        if x>W: x=-size
        fog_particles[i] = [fog_surface,x,y,speed,base_size,pulse_speed,pulse_phase]
        screen.blit(fog_surface,(x,y))
# ---------------------- MARS HORIZON ----------------------
horizon_surface = pygame.Surface((W*2,200),pygame.SRCALPHA)
for x in range(0,W*2,64):
    pygame.draw.rect(horizon_surface, MARS_ORANGE, (x,50,64,150))
horizon_x = 0
horizon_speed = 0.2

# ---------------------- METEOR SYSTEM ----------------------
meteors = []

def spawn_meteor():
    x = -50
    y = random.randint(0,H//2)
    size = random.randint(3,8)
    speed = random.uniform(4,9)
    meteors.append([x,y,size,speed])

def draw_meteors(screen):
    for m in meteors[:]:
        x,y,size,speed = m
        pygame.draw.circle(screen,(255,200,50),(int(x),int(y)),size)
        x += speed
        y += speed*0.3
        if x>W+50 or y>H: meteors.remove(m)
        else: m[0],m[1] = x,y

def show_title():
    title_font = pygame.font.SysFont('Impact', 100, bold=False)  # title жұмсақ, қатты емес
    subtitle_font = pygame.font.SysFont('Courier New', 30, bold=False)  # subtitle да жұмсақ

    glow_phase = 0
    timer = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN: return

        # ---------- Фон ----------
        screen.fill(MARS_RED)
        draw_fog(screen)
        if random.random() < 0.03: spawn_meteor()
        draw_meteors(screen)

        # ---------- Glow effect ----------
        glow_phase += 0.05
        glow_intensity = 180 + int(50 * math.sin(glow_phase))  # жұмсақ жарқырау

        # ---------- Title ----------
        title_color = (glow_intensity, 50, 50)  # қызыл-қызғылт
        title_text = title_font.render("DOOM: Red Inferno", True, title_color)
        screen.blit(title_text, (W//2 - title_text.get_width()//2, H//2 - 60))

        # ---------- Subtitle ----------
        subtitle_color = (255, 180, 100)  # жұмсақ сары-қызғылт
        subtitle_text = subtitle_font.render("Created by Redstone Unit", True, subtitle_color)
        screen.blit(subtitle_text, (W//2 - subtitle_text.get_width()//2, H//2 + 60))

        pygame.display.flip()
        clock.tick(FPS)
        timer += 1
        if timer > 250: break  # титр 4-5 секундтен кейін өтіп кетеді






# ---------------------- CUTSCENE ----------------------
def intro_cutscene():
    texts = ["Данная игра создана с помощью ИИ  и наша комманда Redstone Unit. ",
             "Члены комманды: Abdurakhman Sagyngaliev(TeamLeader and Programmer)",
             "Damir Serikuly(Game Designer)",
             "Elburikhan Nurzhanov(Technical Assistant)",
             "Dinmukhammed Farkhatuly(Story Assistant)",
             "Yusuf Nurgali(Visual Assistant)",
             "...Начинается...",
             "...2147 год...",
             "Человечество построило на Марсе полноценную военную и исследовательскую базу.",
             "Нам нужно управлять энергией портала.",
             "Но за одну ночь всё изменилось.",
             "Эксперимент прошёл неудачно...",
             "Портал открылся, подземные существа ада переместились на Марс.",
             "База потеряла связь...",
             "Все солдаты… либо погибли, либо превратились в чудовищ.",
             "Выжил только один человек — ты.",
             "У тебя осталось один пистолет с бесконечными патронами.",
             "Тебе нужно уничтожить всех монстров, особенно босса.",
             "После того как ты полностью уничтожишь всех,",
             "ты автоматически отправляешься к ракете и возвращаешься на Землю.",
             "Не бойся, ты победишь!"]

    overlay = pygame.Surface((W, H))
    overlay.fill(BLACK)
    alpha = 255
    phase = 0
    timer = 0


    # Шрифты
    main_font = pygame.font.SysFont('Georgia', 30, italic=True)
    small_font = pygame.font.SysFont('Comic Sans MS', 12, bold=True)

    global horizon_x

    while True:
        dt = clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN: return

        # ---------- Фон ----------
        screen.fill(MARS_RED)

        # ---------- Горизонт ----------
        horizon_x -= horizon_speed
        if horizon_x <= -W: horizon_x = 0
        screen.blit(horizon_surface, (horizon_x, H-200))
        screen.blit(horizon_surface, (horizon_x + W*2, H-200))

        # ---------- Туман ----------
        draw_fog(screen)

        # ---------- Метеориттер ----------
        if random.random() < 0.03: spawn_meteor()
        draw_meteors(screen)

        # ---------- Overlay ----------
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))

        # ---------- Основной текст ----------
        t = main_font.render(texts[phase], True, WHITE)
        screen.blit(t, (W // 2 - t.get_width() // 2, H // 2 - 40))

        # ---------- Подсказка ----------
        small = small_font.render("Чтобы пропустить заставку, нажмите Enter", True, WHITE)
        screen.blit(small, (W // 2 - small.get_width() // 2, H // 2 + 40))

        pygame.display.flip()

        # ---------- Таймер ----------
        timer += 1
        if timer % 60 == 0: alpha = max(0, alpha - 12)
        if timer % 180 == 0:
            phase += 1
            if phase >= len(texts): break

    pygame.time.delay(600)


# ---------------------- GAME FUNCTIONS ----------------------
def game_over():
    pygame.mixer.music.stop()
    while True:
        screen.fill(DARK_RED)
        t = pygame.font.SysFont('Impact',55).render('ВЫ УМЕРЛИ!!!',True,RED)
        info = pygame.font.SysFont('Comic Sans MS',16).render('«Enter - Заново | Esc - Выйти»',True,WHITE)
        screen.blit(t,(W//2 - t.get_width()//2,H//2-40))
        screen.blit(info,(W//2 - info.get_width()//2,H//2+20))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN: main()
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

def you_win():
    pygame.mixer.music.stop()
    while True:
        screen.fill(BLACK)
        t = pygame.font.SysFont('Impact',55).render('ВЫ ВЫИГРАЛИ!!!',True,GREEN)
        info = pygame.font.SysFont('Comic Sans MS',16).render('«Нажмите Esc для выхода»',True,WHITE)
        screen.blit(t,(W//2 - t.get_width()//2,H//2-40))
        screen.blit(info,(W//2 - info.get_width()//2,H//2+20))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()


def show_wave_title(title):
    timer = 0
    # Мұнда шрифтті Courier New етіп қойдық
    font = pygame.font.SysFont("Courier New", 60,bold=True)

    while timer < 120:  # 2 секунд
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        screen.fill(MARS_RED)
        draw_fog(screen)

        # ---------- Glow эффект ----------
        glow_intensity = 180 + int(75 * math.sin(timer * 0.1))
        color = (glow_intensity, glow_intensity, glow_intensity)
        text = font.render(title, True, color)

        # Текст ортасына шығару
        screen.blit(text, (W//2 - text.get_width()//2, H//2 - text.get_height()//2))

        pygame.display.flip()
        clock.tick(FPS)
        timer += 1





def spawn_wave(wave, enemies_list):
    spawn_points = [(100, 100), (W - 100, 100), (100, H - 100), (W - 100, H - 100)]

    for enemy_type, count in wave["enemies"]:
        count *= 5  # монстрларды 2 есеге көбейту
        for _ in range(count):
            sp = random.choice(spawn_points)
            x_offset = random.randint(-40, 40)
            y_offset = random.randint(-40, 40)
            if enemy_type == "imp":
                enemies_list.append(Enemy(sp[0] + x_offset, sp[1] + y_offset, 35, 1.2, 12, IMP_SPR))
            elif enemy_type == "caco":
                enemies_list.append(Enemy(sp[0] + x_offset, sp[1] + y_offset, 120, 0.6, 25, CACO_SPR))
            elif enemy_type == "final":
                enemies_list.append(Enemy(W // 2, H // 4, 2000, 0.5, 40, FINAL_SPR))


# ---------------------- MAIN ----------------------
def main():
    global current_level
    player = Player(W//2,H//2)
    enemies = []
    bullets = []

    # ---------------------- WAVES ----------------------
    waves = [
        {"name": "First wave", "enemies": [("imp", 5)]},
        {"name": "Second wave", "enemies": [("caco", 4)]},
        {"name": "Third wave", "enemies": [("imp", 8), ("caco", 5)]},
        {"name": "FINAL!!!", "enemies": [("final", 1)]},
    ]

    current_wave = 0
    final_boss_spawned = False
    final_boss = None

    show_title()
    intro_cutscene()
    stop_bg_music()
    pygame.mixer.music.stop()  # заставка музыкасын тоқтату
    game_music()  # ойын музыкасын қосу

    # Алғашқы волнаны spawn жасаймыз
    spawn_wave(waves[current_wave], enemies)
    show_wave_title(waves[current_wave]["name"])
    wave_active = True

    running = True
    while running:
        dt = clock.tick(FPS)

        # ---------- Events ----------
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: running=False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE: running=False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    play_shoot()
                    mx,my = pygame.mouse.get_pos()
                    ang = math.atan2(my-player.y, mx-player.x)
                    bullets.append(Bullet(player.x + math.cos(ang)*18, player.y + math.sin(ang)*18, ang))

        # ---------- Player movement ----------
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]: dy -= player.speed
        if keys[pygame.K_s]: dy += player.speed
        if keys[pygame.K_a]: dx -= player.speed
        if keys[pygame.K_d]: dx += player.speed
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        player.move(dx, dy)

        # ---------- Update bullets ----------
        to_remove_bullets = []
        for b in bullets:
            b.update()
            for e in enemies[:]:
                if math.hypot(e.x-b.x, e.y-b.y) <= e.radius + b.radius:
                    e.hp -= b.dmg
                    if b not in to_remove_bullets: to_remove_bullets.append(b)
                    if e.hp <= 0:
                        enemies.remove(e)
                        player.score += 5
        for b in to_remove_bullets:
            if b in bullets: bullets.remove(b)

        # ---------- Update enemies ----------
        for e in enemies[:]:
            e.update(player)
            if math.hypot(e.x-player.x, e.y-player.y) <= player.radius + e.radius:
                player.hp -= 6
                if e != final_boss:
                    enemies.remove(e)
            if hasattr(e, 'update_animation'): e.update_animation()
        if hasattr(player, 'update_animation'): player.update_animation()

        # ---------- Wave progress ----------
        if wave_active and len(enemies) == 0:
            wave_active = False
            current_wave += 1

            if current_wave >= len(waves):
                play_win()
                you_win()
                return
            else:
                show_wave_title(waves[current_wave]["name"])
                spawn_wave(waves[current_wave], enemies)
                wave_active = True

                # Final boss тек 5-ші волнада
                if current_wave == 4 and not final_boss_spawned:
                    final_boss_spawned = True
                    final_boss = Enemy(W//2,H//4,2000,0.5,40,FINAL_SPR)
                    enemies.append(final_boss)

        # ---------- Drawing ----------
        # Background
        for x in range(0,W,64):
            for y in range(0,H,64):
                screen.blit(floor_tex,(x,y))

        # Enemies and bullets
        for e in enemies: e.draw(screen)
        for b in bullets: b.draw(screen)
        player.draw(screen,current_wave)

        # ---------- Mini-map ----------
        RADAR_X = W - 150
        RADAR_Y = 130
        RADAR_R = 110
        pygame.draw.circle(screen, (100, 30, 30), (RADAR_X, RADAR_Y), RADAR_R)
        pygame.draw.circle(screen, (180, 60, 60), (RADAR_X, RADAR_Y), RADAR_R, 2)
        for e in enemies:
            rx = (e.x - player.x) * 0.07
            ry = (e.y - player.y) * 0.07
            ex = int(RADAR_X + rx)
            ey = int(RADAR_Y + ry)
            if (ex - RADAR_X) ** 2 + (ey - RADAR_Y) ** 2 <= RADAR_R ** 2:
                pygame.draw.circle(screen, RED, (ex, ey), 5)

        # Player arrow
        mx, my = pygame.mouse.get_pos()
        player_angle = math.atan2(my - player.y, mx - player.x)
        draw_player_arrow(screen, RADAR_X, RADAR_Y, player_angle)

        pygame.display.flip()

        # ---------- Game over / win ----------
        if player.hp <= 0:
            play_lose()
            game_over()
            return
        if final_boss_spawned and final_boss not in enemies:
            play_win()
            you_win()
            return

    pygame.quit(); sys.exit()

if __name__=='__main__':
    main()