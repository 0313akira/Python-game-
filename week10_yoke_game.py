# 第8〜10週の成果物：よけゲーム（Pygame）
# 使う知識：ゲームループ、キー入力、当たり判定、スコア表示、効果音
#
# 遊び方
#   スペースキーでスタート
#   ← → キー（または A / D）で宇宙船を左右に動かす
#   上から落ちてくる隕石をよけて、星を拾う
#   隕石に当たったらゲームオーバー。スペースキーでもう一度、Esc で終了
#
# スコア
#   生き残った 1 秒ごとに 1 点、星を 1 つ拾うごとに 5 点
#
# 準備: pip install pygame
#
# メモ: 画面の文字は英語にしている。Pygame の標準フォントは
#       日本語を表示できないため（日本語にしたい場合は README を参照）。
#       画像ファイルや音声ファイルは使わず、絵も音もプログラムで作っている。

import array
import math
import random
from pathlib import Path

import pygame

# ---- 設定（ここの数字を変えると、ゲームの感じが変わる） ----
WIDTH, HEIGHT = 480, 640       # 画面の大きさ
FPS = 60                       # 1秒あたりの描画回数
PLAYER_SIZE = 40
PLAYER_SPEED = 6
START_FALL_SPEED = 3           # 最初の隕石の落ちる速さ
START_SPAWN_INTERVAL = 30      # 最初は何フレームごとに隕石を出すか
MIN_SPAWN_INTERVAL = 10        # いちばん難しくなったときの間隔
STAR_INTERVAL = FPS * 3        # 星は約3秒ごとに出る
STAR_POINTS = 5                # 星1つの点数

# 色（赤, 緑, 青）
BG_COLOR = (14, 16, 32)
PLAYER_COLOR = (80, 200, 255)
FLAME_COLOR = (255, 180, 60)
ROCK_COLOR = (170, 120, 95)
CRATER_COLOR = (120, 82, 65)
STAR_COLOR = (255, 225, 70)
TEXT_COLOR = (240, 240, 240)
SUB_TEXT_COLOR = (160, 170, 200)

SCORE_FILE = Path(__file__).parent / "yoke_highscore.txt"


# ---------------------------------------------------------------
# ハイスコアの保存と読み込み
# ---------------------------------------------------------------
def load_highscore():
    if SCORE_FILE.exists():
        text = SCORE_FILE.read_text(encoding="utf-8").strip()
        if text.isdigit():
            return int(text)
    return 0


def save_highscore(score):
    SCORE_FILE.write_text(str(score), encoding="utf-8")


# ---------------------------------------------------------------
# 効果音：音声ファイルを使わず、波の形を計算して音を作る
# ---------------------------------------------------------------
class Sounds:
    def __init__(self):
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
        except pygame.error:
            return  # 音が出せない環境では、音なしで遊べるようにする
        self.sounds["star"] = self.make_tone(660, 1320, 120)   # 高くなる「ピロッ」
        self.sounds["hit"] = self.make_tone(220, 40, 400)      # 低くなる「ドーン」
        self.sounds["start"] = self.make_tone(440, 880, 150)

    def make_tone(self, start_freq, end_freq, ms, volume=0.25):
        """start_freq から end_freq へ音の高さが変わる短い音を作る。"""
        rate, _, channels = pygame.mixer.get_init()
        count = int(rate * ms / 1000)
        samples = array.array("h")
        phase = 0.0
        for i in range(count):
            t = i / count                                   # 0 → 1 に進む
            freq = start_freq + (end_freq - start_freq) * t
            phase += freq / rate
            wave = 1 if phase % 1 < 0.5 else -1             # 矩形波（ピコピコ音）
            value = int(wave * volume * (1 - t) * 32767)    # だんだん小さく
            for _ in range(channels):
                samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()


# ---------------------------------------------------------------
# ゲームに出てくるもの
# ---------------------------------------------------------------
class Player:
    def __init__(self):
        x = WIDTH // 2 - PLAYER_SIZE // 2
        y = HEIGHT - PLAYER_SIZE - 24
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        # 画面の外に出ないようにする
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))

    def hitbox(self):
        # 見た目より少し小さい当たり判定にすると、遊んでいて気持ちいい
        return self.rect.inflate(-12, -10)

    def draw(self, surface, frame):
        r = self.rect
        # エンジンの炎（フレームごとに長さを変えてゆらゆらさせる）
        flame = 8 + (frame // 3) % 3 * 4
        pygame.draw.polygon(surface, FLAME_COLOR, [
            (r.centerx - 7, r.bottom - 4),
            (r.centerx + 7, r.bottom - 4),
            (r.centerx, r.bottom + flame),
        ])
        # 機体（三角形）と窓
        pygame.draw.polygon(surface, PLAYER_COLOR, [
            (r.centerx, r.top),
            (r.right, r.bottom),
            (r.centerx, r.bottom - 8),
            (r.left, r.bottom),
        ])
        pygame.draw.circle(surface, BG_COLOR, (r.centerx, r.centery + 2), 5)


class Rock:
    """落ちてくる隕石。大きさと速さが1つずつ違う。"""

    def __init__(self, base_speed, max_size):
        size = random.randint(24, max_size)
        x = random.randint(0, WIDTH - size)
        self.rect = pygame.Rect(x, -size, size, size)
        self.speed = base_speed + random.random() * 1.5
        self.y = float(self.rect.y)  # 小数で位置を持つと、なめらかに動く
        # クレーター（くぼみ）の位置を、作ったときに決めておく
        self.craters = [
            (random.randint(-size // 4, size // 4),
             random.randint(-size // 4, size // 4),
             random.randint(2, max(3, size // 7)))
            for _ in range(3)
        ]

    def update(self):
        self.y += self.speed
        self.rect.y = int(self.y)

    def is_off_screen(self):
        return self.rect.top > HEIGHT

    def hitbox(self):
        return self.rect.inflate(-6, -6)

    def draw(self, surface):
        radius = self.rect.width // 2
        pygame.draw.circle(surface, ROCK_COLOR, self.rect.center, radius)
        for dx, dy, cr in self.craters:
            pygame.draw.circle(surface, CRATER_COLOR,
                               (self.rect.centerx + dx, self.rect.centery + dy), cr)


class Star:
    """拾うと点数が入る星。くるくる回りながら落ちてくる。"""

    SIZE = 28

    def __init__(self):
        x = random.randint(0, WIDTH - self.SIZE)
        self.rect = pygame.Rect(x, -self.SIZE, self.SIZE, self.SIZE)
        self.speed = 2.5
        self.y = float(self.rect.y)
        self.angle = 0.0

    def update(self):
        self.y += self.speed
        self.rect.y = int(self.y)
        self.angle += 0.05

    def is_off_screen(self):
        return self.rect.top > HEIGHT

    def draw(self, surface):
        cx, cy = self.rect.center
        points = []
        for i in range(10):  # 外側と内側の点を交互に並べると星の形になる
            r = self.SIZE / 2 if i % 2 == 0 else self.SIZE / 5
            a = self.angle + i * math.pi / 5 - math.pi / 2
            points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        pygame.draw.polygon(surface, STAR_COLOR, points)


class PopText:
    """星を拾ったときに出る「+5」の文字。少し浮かんで消える。"""

    def __init__(self, text, pos, font):
        self.image = font.render(text, True, STAR_COLOR)
        self.x, self.y = pos
        self.life = 40  # 何フレーム表示するか

    def update(self):
        self.y -= 1
        self.life -= 1

    def draw(self, surface):
        self.image.set_alpha(int(255 * self.life / 40))
        surface.blit(self.image, self.image.get_rect(center=(self.x, self.y)))


class Background:
    """奥から流れてくる星空。速さの違う点を混ぜると奥行きが出る。"""

    def __init__(self):
        self.dots = [[random.randint(0, WIDTH), random.randint(0, HEIGHT),
                      random.choice([0.5, 1, 2])] for _ in range(70)]

    def update(self):
        for dot in self.dots:
            dot[1] += dot[2]
            if dot[1] > HEIGHT:
                dot[0] = random.randint(0, WIDTH)
                dot[1] = 0

    def draw(self, surface):
        surface.fill(BG_COLOR)
        for x, y, speed in self.dots:
            shade = 90 + int(speed * 60)
            pygame.draw.circle(surface, (shade, shade, shade + 20), (int(x), int(y)),
                               1 if speed < 2 else 2)


# ---------------------------------------------------------------
# ゲーム全体
# ---------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Yoke Game")
        # 一度 canvas に描いてから画面に貼る（画面を揺らすため）
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 72)
        self.sounds = Sounds()
        self.background = Background()
        self.highscore = load_highscore()
        self.state = "title"  # "title"（タイトル）→ "play"（プレイ中）→ "over"（ゲームオーバー）
        self.reset()

    def reset(self):
        """新しいゲームを始める準備をする。"""
        self.player = Player()
        self.rocks = []
        self.stars = []
        self.pops = []
        self.frame = 0
        self.bonus = 0          # 星で増えた点数
        self.score = 0
        self.shake = 0          # 画面の揺れの強さ
        self.flash = 0          # 画面が赤く光る強さ
        self.new_record = False

    # ---- 難しさ：時間がたつほど上がる ----
    def level(self):
        return self.frame // (FPS * 10)  # 10秒ごとに 1 つ上がる

    def fall_speed(self):
        return START_FALL_SPEED + self.level() * 0.8

    def spawn_interval(self):
        return max(MIN_SPAWN_INTERVAL, START_SPAWN_INTERVAL - self.level() * 4)

    def max_rock_size(self):
        return min(64, 36 + self.level() * 6)

    # ---- 毎フレームの更新 ----
    def update(self):
        self.background.update()
        for pop in self.pops:
            pop.update()
        self.pops = [p for p in self.pops if p.life > 0]
        self.shake = max(0, self.shake - 1)
        self.flash = max(0, self.flash - 8)

        if self.state != "play":
            return

        self.frame += 1
        self.score = self.frame // FPS + self.bonus

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        if self.frame % self.spawn_interval() == 0:
            self.rocks.append(Rock(self.fall_speed(), self.max_rock_size()))
        if self.frame % STAR_INTERVAL == 0:
            self.stars.append(Star())

        for thing in self.rocks + self.stars:
            thing.update()
        self.rocks = [r for r in self.rocks if not r.is_off_screen()]
        self.stars = [s for s in self.stars if not s.is_off_screen()]

        # 星を拾ったか
        for star in self.stars[:]:
            if self.player.rect.colliderect(star.rect):
                self.stars.remove(star)
                self.bonus += STAR_POINTS
                self.sounds.play("star")
                self.pops.append(PopText(f"+{STAR_POINTS}", star.rect.center, self.font))

        # 隕石に当たったか
        for rock in self.rocks:
            if self.player.hitbox().colliderect(rock.hitbox()):
                self.end_game()
                break

    def end_game(self):
        self.state = "over"
        self.shake = 20
        self.flash = 200
        self.sounds.play("hit")
        if self.score > self.highscore:
            self.highscore = self.score
            self.new_record = True
            save_highscore(self.highscore)

    # ---- 描画 ----
    def draw_center(self, text, font, y, color=TEXT_COLOR):
        image = font.render(text, True, color)
        self.canvas.blit(image, image.get_rect(center=(WIDTH // 2, y)))

    def draw(self):
        self.background.draw(self.canvas)

        if self.state == "title":
            self.draw_center("YOKE GAME", self.big_font, HEIGHT // 2 - 80)
            self.draw_center("Dodge the rocks, grab the stars", self.small_font,
                             HEIGHT // 2 - 20, SUB_TEXT_COLOR)
            self.draw_center("Move: LEFT / RIGHT  (A / D)", self.small_font,
                             HEIGHT // 2 + 20, SUB_TEXT_COLOR)
            if (pygame.time.get_ticks() // 500) % 2 == 0:  # 点滅させる
                self.draw_center("Press SPACE to start", self.font, HEIGHT // 2 + 90)
            self.draw_center(f"Best: {self.highscore}", self.small_font, HEIGHT - 40,
                             SUB_TEXT_COLOR)
        else:
            for star in self.stars:
                star.draw(self.canvas)
            for rock in self.rocks:
                rock.draw(self.canvas)
            self.player.draw(self.canvas, self.frame)
            for pop in self.pops:
                pop.draw(self.canvas)

            self.canvas.blit(self.font.render(f"Score: {self.score}", True, TEXT_COLOR), (12, 12))
            self.canvas.blit(self.small_font.render(f"Best: {self.highscore}", True,
                                                    SUB_TEXT_COLOR), (12, 44))
            self.canvas.blit(self.small_font.render(f"Level {self.level() + 1}", True,
                                                    SUB_TEXT_COLOR), (WIDTH - 90, 14))

            if self.state == "over":
                self.draw_center("GAME OVER", self.big_font, HEIGHT // 2 - 40)
                if self.new_record:
                    self.draw_center("NEW RECORD!", self.font, HEIGHT // 2 + 10, STAR_COLOR)
                self.draw_center("SPACE: retry   ESC: quit", self.small_font,
                                 HEIGHT // 2 + 50, SUB_TEXT_COLOR)

        # 当たったときは画面を赤く光らせる
        if self.flash > 0:
            red = pygame.Surface((WIDTH, HEIGHT))
            red.fill((255, 40, 40))
            red.set_alpha(self.flash)
            self.canvas.blit(red, (0, 0))

        # 揺れているときは、少しずらして貼る
        offset = (0, 0)
        if self.shake > 0:
            offset = (random.randint(-self.shake, self.shake),
                      random.randint(-self.shake, self.shake))
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.canvas, offset)
        pygame.display.flip()

    # ---- メインループ ----
    def run(self):
        running = True
        while running:
            # 1. 入力を受け取る
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and self.state != "play":
                        self.reset()
                        self.state = "play"
                        self.sounds.play("start")
            # 2. ゲームの状態を更新する
            self.update()
            # 3. 画面に描く
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
