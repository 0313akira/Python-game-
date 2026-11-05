# 第8〜10週の成果物：よけゲーム（Pygame）
# 使う知識：ゲームループ、キー入力、当たり判定、スコア表示
#
# 遊び方
#   ← → キー（または A / D）でプレイヤーを左右に動かす
#   上から落ちてくるブロックをよける
#   当たったらゲームオーバー。スペースキーでもう一度
#
# 準備: pip install pygame
#
# メモ: 画面の文字は英語にしている。Pygame の標準フォントは
#       日本語を表示できないため（日本語にしたい場合は README を参照）。

import random
from pathlib import Path

import pygame

# ---- 設定（ここの数字を変えると、ゲームの感じが変わる） ----
WIDTH, HEIGHT = 480, 640       # 画面の大きさ
FPS = 60                       # 1秒あたりの描画回数
PLAYER_SIZE = 40
PLAYER_SPEED = 6
BLOCK_SIZE = 36
START_FALL_SPEED = 3           # 最初の落ちる速さ
SPAWN_INTERVAL = 30            # 何フレームごとにブロックを出すか

# 色（赤, 緑, 青）
BG_COLOR = (20, 24, 40)
PLAYER_COLOR = (80, 200, 255)
BLOCK_COLOR = (255, 110, 90)
TEXT_COLOR = (240, 240, 240)

SCORE_FILE = Path(__file__).parent / "yoke_highscore.txt"


def load_highscore():
    if SCORE_FILE.exists():
        text = SCORE_FILE.read_text(encoding="utf-8").strip()
        if text.isdigit():
            return int(text)
    return 0


def save_highscore(score):
    SCORE_FILE.write_text(str(score), encoding="utf-8")


class Player:
    def __init__(self):
        x = WIDTH // 2 - PLAYER_SIZE // 2
        y = HEIGHT - PLAYER_SIZE - 20
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        # 画面の外に出ないようにする
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect, border_radius=8)


class Block:
    def __init__(self, speed):
        x = random.randint(0, WIDTH - BLOCK_SIZE)
        self.rect = pygame.Rect(x, -BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.top > HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, BLOCK_COLOR, self.rect, border_radius=6)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Yoke Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 64)
        self.highscore = load_highscore()
        self.reset()

    def reset(self):
        """新しいゲームを始める準備をする。"""
        self.player = Player()
        self.blocks = []
        self.frame = 0
        self.score = 0
        self.game_over = False

    def fall_speed(self):
        # 時間がたつほど速くなる（10秒ごとに +1）
        return START_FALL_SPEED + self.frame // (FPS * 10)

    def update(self):
        if self.game_over:
            return

        self.frame += 1
        self.score = self.frame // FPS  # 生き残った秒数がスコア

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        if self.frame % SPAWN_INTERVAL == 0:
            self.blocks.append(Block(self.fall_speed()))

        for block in self.blocks:
            block.update()
        self.blocks = [b for b in self.blocks if not b.is_off_screen()]

        # 当たり判定
        for block in self.blocks:
            if self.player.rect.colliderect(block.rect):
                self.game_over = True
                if self.score > self.highscore:
                    self.highscore = self.score
                    save_highscore(self.highscore)
                break

    def draw_text(self, text, font, y):
        image = font.render(text, True, TEXT_COLOR)
        rect = image.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(image, rect)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.player.draw(self.screen)
        for block in self.blocks:
            block.draw(self.screen)

        score_image = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        best_image = self.font.render(f"Best: {self.highscore}", True, TEXT_COLOR)
        self.screen.blit(score_image, (12, 12))
        self.screen.blit(best_image, (12, 44))

        if self.game_over:
            self.draw_text("GAME OVER", self.big_font, HEIGHT // 2 - 30)
            self.draw_text("Press SPACE to retry", self.font, HEIGHT // 2 + 20)

        pygame.display.flip()

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
                    elif event.key == pygame.K_SPACE and self.game_over:
                        self.reset()
            # 2. ゲームの状態を更新する
            self.update()
            # 3. 画面に描く
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
