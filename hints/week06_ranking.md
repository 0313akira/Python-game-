# 第6週 ランキング付き数当て：ヒントと解説

サンプル: [`week06_kazuate_highscore.py`](../week06_kazuate_highscore.py)

## 作るもの

第4週の数当てゲームに、**プログラムを閉じても消えない記録**を付ける。

まずは「いちばん少ない回数を1つだけ保存する」ハイスコア版を作りましょう。
上位5位のランキングは、そのあとの発展です。

## ヒント

<details>
<summary>ヒント1：何が必要か</summary>

- ファイルに書く → `Path("highscore.txt").write_text("12")`
- ファイルを読む → `Path("highscore.txt").read_text()`
- ファイルがあるか調べる → `Path("highscore.txt").exists()`
- 最初に `from pathlib import Path` を書く

ファイルには文字しか書けません。数は `str()` で文字にして保存し、読んだら `int()` で数に戻します。

</details>

<details>
<summary>ヒント2：全体の流れ</summary>

1. ファイルがあれば読んで `best` に入れる。なければ `best = None`
2. ゲームを遊んで、かかった回数 `count` を得る
3. `best` が `None`（初めて）か、`count < best`（新記録）なら、ファイルに保存する

ゲーム部分は第4週のコードを関数 `play()` にまとめて、最後に `return count` すると使いやすくなります。

</details>

<details>
<summary>ヒント3：ほぼ答え</summary>

```python
from pathlib import Path

SCORE_FILE = Path("highscore.txt")

if SCORE_FILE.exists():
    best = int(SCORE_FILE.read_text())
else:
    best = None

count = play()   # 第4週のゲームを関数にしたもの

if best is None or count < best:
    print("新記録！")
    SCORE_FILE.write_text(str(count))
```

</details>

## 解説

### ファイルの場所：`Path(__file__).parent`

`Path("ranking.txt")` だけだと、**プログラムを実行した場所**にファイルができます。
実行する場所が変わるたびに、別のファイルになってしまいます。

```python
RANKING_FILE = Path(__file__).parent / "ranking.txt"
```

`__file__` は「このプログラム自身のファイル」、`.parent` は「それが入っているフォルダ」です。
こう書くと、いつもプログラムと同じフォルダに保存されます。

### `encoding="utf-8"`

日本語の名前を保存するので、文字の形式（文字コード）を指定しています。
指定しないと、Windows で文字化けやエラーが起きることがあります。

### ランキングの形：タプルのリスト

```python
ranking = [("あきら", 6), ("ゆう", 8), ("みき", 11)]
```

`("あきら", 6)` のように `( )` でまとめたものを**タプル**と言います。リストと似ていますが、中身を書きかえられません。

ファイルには1行に1人、`あきら,6` の形で書いています。読むときは `split(",")` でカンマで分けます。

```python
"あきら,6".split(",")   # → ["あきら", "6"]
```

### 並べ替えて上位5人だけ残す

```python
ranking.append((name, count))
ranking.sort(key=lambda item: item[1])   # 回数（2番目）で並べる
ranking = ranking[:5]                    # 前から5人だけ
```

- `sort(key=...)` は「何を基準に並べるか」を指定します。`lambda item: item[1]` は「タプルの2番目（回数）で」という意味の短い関数です。
- `[:5]` は「前から5個」を取り出す書き方（スライス）です。

### ランキングに入れるかの判定

```python
if len(ranking) < RANKING_SIZE or count < ranking[-1][1]:
```

- まだ5人いなければ、だれでも入れる
- 5人いれば、5位（`ranking[-1]`、最後の人）の回数より少なければ入れる

`[-1]` は「最後」、`[1]` は「タプルの2番目（回数）」です。

## よくあるエラー

| 症状 | 原因と直し方 |
| --- | --- |
| `FileNotFoundError` | ファイルがないのに読もうとしています。先に `exists()` で調べます |
| `ValueError: invalid literal for int()` | ファイルの中身が数字ではありません。ファイルを消すか、中身を確かめます |
| `TypeError: '<' not supported between instances of 'int' and 'NoneType'` | `best` が `None` のまま比べています。`best is None or count < best` の順に書くと、`None` のときは後ろを調べません |
| 記録が毎回リセットされる | 実行する場所によって別のファイルを見ています。`Path(__file__).parent` を使います |
| 名前が文字化けする | `read_text` と `write_text` の両方に `encoding="utf-8"` を付けます |

## 練習問題のヒント

<details>
<summary>難易度ごとに別のランキングにする</summary>

いちばん簡単なのは、ファイルを分けることです。

```python
RANKING_FILE = Path(__file__).parent / f"ranking_{level}.txt"
```

難易度を選んだあとに、そのファイル名で `load_ranking()` と `save_ranking()` を呼ぶようにします。
そのためには、関数がファイル名を引数で受け取れるように書きかえる必要があります。

</details>
