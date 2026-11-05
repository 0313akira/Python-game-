# Python ゲームで学ぶ 12 週間

Python 学習計画書の「成果物」に合わせたサンプルゲーム集です。
各週の課題を自分で作ったあとに、答え合わせとして読んでください。

| 週 | ファイル | 内容 | 使う知識 |
| --- | --- | --- | --- |
| 4 | `week04_kazuate.py` | 数当てゲーム | 変数、if、while、random |
| 5 | `week05_janken.py` | じゃんけんゲーム（5回勝負） | 関数、リスト、辞書 |
| 6 | `week06_kazuate_highscore.py` | ハイスコア付き数当て | ファイル保存 |
| 7 | `week07_text_battle.py` | 文字バトルゲーム（勇者 vs モンスター） | クラス |
| 8〜10 | `week10_yoke_game.py` | 落ちてくるブロックをよけるゲーム | Pygame、当たり判定 |
| 11〜12 | 自分で作る | オリジナルゲーム | ここまでの全部 |

## 動かし方

```bash
# 第4〜7週（Python だけで動く）
python week04_kazuate.py

# 第8〜10週（Pygame が必要）
pip install pygame
python week10_yoke_game.py
```

よけゲームの操作: ← → キー（または A / D）で移動、スペースでリトライ、Esc で終了。

## おすすめの改造（練習問題）

- 数当て: 範囲を 1〜1000 にする / 10 回で当たらなければ負けにする
- じゃんけん: 先に 3 勝したほうが勝ちにする
- 文字バトル: 魔法（MP を使う強い攻撃）を追加する
- よけゲーム:
  - 画像を使う: `pygame.image.load("player.png")` で四角の代わりに絵を表示する
  - 音を鳴らす: `pygame.mixer.Sound("hit.wav").play()` で当たったときに音を出す
  - 日本語を表示する: `pygame.font.SysFont("meiryo", 36)`（Windows）や
    `pygame.font.SysFont("hiraginosans", 36)`（Mac）を使う
  - 星を拾うとスコアが増えるアイテムを追加する

## 第11〜12週：オリジナルゲーム

1. 作りたいゲームを 3 行で書く（何をするゲームか / 操作 / 勝ち負け）
2. `week10_yoke_game.py` をコピーして、新しいファイル名で始める
3. 「動く最小のもの」を先に作り、少しずつ足していく
4. できたら GitHub にコミットして公開する
