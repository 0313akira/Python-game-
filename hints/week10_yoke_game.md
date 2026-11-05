# 第8〜10週 よけゲーム（Pygame）：ヒントと解説

サンプル: [`week10_yoke_game.py`](../week10_yoke_game.py)

サンプルは 400 行以上あり、最初から全部読むと大変です。週ごとに小さく作っていきましょう。

| 週 | 作るもの |
| --- | --- |
| 8 | 画面を開いて、四角をキーで左右に動かす |
| 9 | 上から四角が落ちてきて、当たったらゲームオーバー |
| 10 | スコア、星、効果音、タイトル画面を足す |

## 第8週：四角を動かす

<details>
<summary>ヒント1：ゲームループとは</summary>

ゲームは、次の3つを1秒に60回くり返しています。

1. **入力を受け取る**（キーが押されたか、ウィンドウが閉じられたか）
2. **状態を更新する**（位置を動かす、当たったか調べる）
3. **画面に描く**

この「ずっと回り続けるループ」を**ゲームループ**と言います。

</details>

<details>
<summary>ヒント2：最小のプログラム</summary>

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
clock = pygame.time.Clock()
player = pygame.Rect(220, 580, 40, 40)   # x, y, 幅, 高さ

running = True
while running:
    for event in pygame.event.get():      # 1. 入力
        if event.type == pygame.QUIT:
            running = False

    # 2. 更新（ここでキーを調べて player.x を変える）

    screen.fill((20, 24, 40))             # 3. 描画
    pygame.draw.rect(screen, (80, 200, 255), player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

</details>

<details>
<summary>ヒント3：キーで動かす部分</summary>

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player.x -= 6
if keys[pygame.K_RIGHT]:
    player.x += 6
```

</details>

## 第9週：落ちてくるものと当たり判定

<details>
<summary>ヒント1：たくさんの「落ちてくるもの」を扱う</summary>

落ちてくる四角を**リスト**に入れて管理します。

- 一定時間ごとに `blocks.append(pygame.Rect(...))` で増やす
- 毎フレーム、リストの全部の `y` を増やす
- 画面の下に出たものはリストから消す

</details>

<details>
<summary>ヒント2：一定時間ごとに出す</summary>

フレーム数を数える変数 `frame` を用意して、毎回 1 増やします。

```python
frame += 1
if frame % 30 == 0:   # 30 で割り切れるとき ＝ 30 フレームに1回 ＝ 0.5 秒に1回
    x = random.randint(0, 480 - 36)
    blocks.append(pygame.Rect(x, -36, 36, 36))
```

</details>

<details>
<summary>ヒント3：当たり判定</summary>

`Rect` 同士なら、`colliderect` で重なっているか調べられます。

```python
for block in blocks:
    block.y += 3
    if player.colliderect(block):
        game_over = True
```

</details>

## 第10週：スコア、星、音、タイトル画面

<details>
<summary>ヒント1：文字を表示する</summary>

```python
font = pygame.font.Font(None, 36)                         # ループの前に1回だけ
image = font.render(f"Score: {score}", True, (240, 240, 240))
screen.blit(image, (12, 12))                              # 左上に貼る
```

`render` で文字を「絵」にして、`blit` で画面に貼ります。

</details>

<details>
<summary>ヒント2：タイトル → プレイ → ゲームオーバーの切り替え</summary>

`state` という変数に今の場面を入れて、場面ごとに動きを変えます。

```python
state = "title"
# スペースが押されたら
if state != "play":
    state = "play"
# 当たったら
state = "over"
```

更新と描画の中で `if state == "play":` のように分けます。

</details>

<details>
<summary>ヒント3：星を拾う</summary>

星も落ちてくる四角と同じしくみで、リスト `stars` で管理します。
違うのは、当たったら**ゲームオーバーではなく、スコアを足して星を消す**ことだけです。

```python
for star in stars[:]:        # [:] でコピーしてからループする（理由は下の解説）
    if player.colliderect(star):
        stars.remove(star)
        bonus += 5
```

</details>

## 解説

### サンプルの全体の形

サンプルは、ゲームに出てくるものをクラスに分けています。

| クラス | 役割 |
| --- | --- |
| `Player` | 宇宙船。キーで動く |
| `Rock` | 隕石。大きさと速さが1つずつ違う |
| `Star` | 星。拾うと点数 |
| `PopText` | 星を拾ったときの「+5」 |
| `Background` | 流れる星空 |
| `Sounds` | 効果音を作って鳴らす |
| `Game` | 全体をまとめる。`update()` で更新、`draw()` で描画、`run()` がゲームループ |

どのクラスも `update()`（動く）と `draw()`（描く）を持っているので、`Game` からは同じ書き方で扱えます。

### ループ中にリストから消すときは `[:]`

```python
for star in self.stars[:]:
    ...
    self.stars.remove(star)
```

ループしている最中のリストから要素を消すと、次の要素が飛ばされることがあります。
`[:]` でコピーを作り、コピーのほうでループすると安全です。

隕石のほうは、別の書き方で消しています。

```python
self.rocks = [r for r in self.rocks if not r.is_off_screen()]
```

これは「画面の外に出ていないものだけで、新しいリストを作る」という意味です。

### 当たり判定を見た目より小さくする

```python
def hitbox(self):
    return self.rect.inflate(-12, -10)
```

宇宙船は三角形ですが、当たり判定は四角です。四角のままだと、角にかすっただけで当たってしまいます。
`inflate` にマイナスを渡すと四角が小さくなり、遊んでいて「今のは当たってないのに」と感じにくくなります。

### 難しさを時間で上げる

```python
def level(self):
    return self.frame // (FPS * 10)   # 600 フレーム（10秒）ごとに 1 上がる
```

落ちる速さ・出てくる間隔・隕石の大きさを、すべて `level()` から計算しています。
数字を1か所変えるだけで、ゲーム全体の難しさを調整できます。

### 画面を揺らすしくみ

いったん `canvas` という別の画面に全部描いてから、本物の画面に**少しずらして**貼っています。
ずらす量 `shake` を毎フレーム 1 ずつ減らすので、揺れがだんだん収まります。

### 音をプログラムで作る

`Sounds.make_tone()` は、音の波の形を数字の並びとして計算しています。
`1` と `-1` を交互に並べると「ピー」というゲーム機のような音（矩形波）になります。
並べる速さを変えると音の高さが変わり、数字を小さくしていくと音がだんだん消えます。

音が出せない環境では `pygame.mixer.init()` がエラーになるので、`try` / `except` で受け止めて、音なしで遊べるようにしています。

## よくあるエラー

| 症状 | 原因と直し方 |
| --- | --- |
| `ModuleNotFoundError: No module named 'pygame'` | `pip install pygame` をします。それでもだめなら `python -m pip install pygame` |
| ウィンドウが一瞬で閉じる | ゲームループ（`while running:`）がないか、すぐ `running = False` になっています |
| ウィンドウが「応答なし」になる | ループの中で `pygame.event.get()` を呼んでいません。毎フレーム必ず呼びます |
| 四角が動いた跡が残る | 毎フレーム最初に `screen.fill(...)` で塗りつぶしていません |
| 何も表示されない | 最後に `pygame.display.flip()` を呼んでいません |
| 動きが速すぎる・パソコンによって速さが違う | `clock.tick(60)` を呼んでいません |
| 日本語が「□□□」になる | 標準フォントは日本語を表示できません。README の「日本語を表示する」を参照 |

## 練習問題のヒント

<details>
<summary>一定時間だけ無敵になるアイテム</summary>

星と同じしくみで、別の色のアイテムを作ります。
拾ったら `self.invincible = FPS * 3`（3秒分）にして、毎フレーム 1 ずつ減らします。
隕石との当たり判定の前に `if self.invincible > 0:` なら判定を飛ばします。
無敵中は宇宙船を点滅させると分かりやすくなります（`if self.invincible % 10 < 5:` のときだけ描く）。

</details>
