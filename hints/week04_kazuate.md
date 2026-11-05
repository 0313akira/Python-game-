# 第4週 数当てゲーム：ヒントと解説

サンプル: [`week04_kazuate.py`](../week04_kazuate.py)

## 作るもの

コンピューターが決めた 1〜100 の数を当てるゲーム。

```
1〜100 の数を当ててね！
数を入力してください: 50
もっと小さいよ。
数を入力してください: 25
正解！ 答えは 25 でした。2 回で当たりました。
```

まずはこの「基本版」を作りましょう。難易度や回数制限は、そのあとの発展です。

## ヒント

<details>
<summary>ヒント1：何が必要か</summary>

必要な部品は4つです。

- 正解の数を決める → `random.randint(1, 100)`
- 入力を受け取る → `input()`
- 大きい・小さい・正解を判定する → `if` / `elif` / `else`
- 当たるまでくり返す → `while`

</details>

<details>
<summary>ヒント2：全体の形</summary>

```python
import random

answer = random.randint(1, 100)

while True:
    # 入力を受け取って、数にする
    # 正解より小さければ「もっと大きいよ」
    # 正解より大きければ「もっと小さいよ」
    # 正解なら「正解！」と表示して、ループを抜ける（break）
```

`while True:` は「ずっとくり返す」という意味です。抜けるときは `break` を使います。

</details>

<details>
<summary>ヒント3：ほぼ答え</summary>

```python
import random

answer = random.randint(1, 100)
count = 0

while True:
    guess = int(input("数を入力してください: "))
    count = count + 1
    if guess < answer:
        print("もっと大きいよ。")
    elif guess > answer:
        print("もっと小さいよ。")
    else:
        print(f"正解！ {count} 回で当たりました。")
        break
```

</details>

## 解説

### `input()` が返すのは「文字」

`input()` で受け取ったものは、数字を打っても**文字（str）**です。
`"50"` と `50` は別物なので、比べる前に `int()` で数に変えます。

```python
text = input("数: ")   # "50"（文字）
guess = int(text)      # 50（数）
```

### 数字以外を入力されたときの対策

`int("abc")` はエラーになります。サンプルでは、先に `isdigit()` で「全部数字か」を確かめています。

```python
if not text.isdigit():
    print("数字を入力してね。")
    continue   # この回の残りを飛ばして、ループの先頭に戻る
```

`continue` は「この回はここで終わり、次の回へ」、`break` は「ループそのものを終わる」です。

### 回数制限と `while 〜 else`

サンプルの完成版では、`while count < tries:` で回数を制限しています。
ループの後ろに付いている `else:` は、**`break` せずにループが終わったときだけ**動きます。
つまり「最後まで当たらなかった」ときの処理を書く場所です。

```python
while count < tries:
    ...
    else:          # ← これは if の else
        print("正解！")
        break
else:              # ← これは while の else（break しなかったときだけ）
    print("残念！")
```

### 難易度を辞書で持つ

```python
LEVELS = {
    "1": ("かんたん", 10, 4),
    "2": ("ふつう", 100, 8),
    "3": ("むずかしい", 1000, 12),
}
name, maximum, tries = LEVELS[choice]
```

`if choice == "1": ... elif choice == "2": ...` と書くこともできますが、辞書にまとめると
難易度を増やすときに1行足すだけで済みます。
右側の `name, maximum, tries = ...` は、3つ組をいっぺんに3つの変数に分ける書き方です。

## よくあるエラー

| 症状 | 原因と直し方 |
| --- | --- |
| `TypeError: '<' not supported between instances of 'str' and 'int'` | `int()` を付け忘れています。`guess = int(input(...))` |
| 正解しても終わらない | `break` を書き忘れているか、`else:` の中に入っていません |
| 何回やっても回数が 0 回のまま | `count = count + 1` がループの外にあるか、ループの中で `count = 0` をしています |
| 正解が毎回同じ | `answer = random.randint(...)` をループの中に書くと、毎回正解が変わってしまいます。ループの前に1回だけ書きます |

## 練習問題のヒント

<details>
<summary>「あと少し！」のヒントを出す（差が 5 以内）</summary>

差の大きさは `abs(guess - answer)` で求められます（`abs` はマイナスを取る関数）。
「もっと大きいよ」を表示する前に、`if abs(guess - answer) <= 5:` で調べてみましょう。

</details>
