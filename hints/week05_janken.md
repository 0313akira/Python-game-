# 第5週 じゃんけんゲーム：ヒントと解説

サンプル: [`week05_janken.py`](../week05_janken.py)

## 作るもの

コンピューターとじゃんけんを何回か勝負して、勝ち・負け・あいこの回数を表示する。

```
--- 1 回戦 ---
1: グー  2: チョキ  3: パー  → 1
あなた: グー  コンピューター: チョキ
あなたの勝ち！
...
結果: 3 勝 1 敗 1 分け
```

まずは「コンピューターはランダムに出す」基本版を作りましょう。クセを読む機能は発展です。

## ヒント

<details>
<summary>ヒント1：何が必要か</summary>

- 手の一覧 → リスト `["グー", "チョキ", "パー"]`
- コンピューターの手 → `random.choice(リスト)`
- 勝ち負けの判定 → 関数にまとめる
- 結果の数え上げ → 辞書 `{"win": 0, "lose": 0, "draw": 0}`
- 5回くり返す → `for i in range(5):`

</details>

<details>
<summary>ヒント2：勝ち負けの判定を短く書くコツ</summary>

「グーはチョキに勝つ」「チョキはパーに勝つ」「パーはグーに勝つ」を辞書にします。

```python
WINS_AGAINST = {"グー": "チョキ", "チョキ": "パー", "パー": "グー"}
```

すると「プレイヤーの勝ち」は `WINS_AGAINST[player] == computer` の1行で調べられます。
同じ手ならあいこ、どちらでもなければ負けです。

</details>

<details>
<summary>ヒント3：ほぼ答え</summary>

```python
import random

HANDS = ["グー", "チョキ", "パー"]
WINS_AGAINST = {"グー": "チョキ", "チョキ": "パー", "パー": "グー"}


def judge(player, computer):
    if player == computer:
        return "draw"
    if WINS_AGAINST[player] == computer:
        return "win"
    return "lose"


results = {"win": 0, "lose": 0, "draw": 0}
for i in range(5):
    number = input("1: グー  2: チョキ  3: パー  → ")
    player = HANDS[int(number) - 1]
    computer = random.choice(HANDS)
    print(f"あなた: {player}  コンピューター: {computer}")
    result = judge(player, computer)
    results[result] = results[result] + 1

print(results)
```

</details>

## 解説

### 関数にまとめる理由

`judge()` のように処理を関数にすると、

- 名前を見るだけで何をしているか分かる
- 何度でも呼べる
- その部分だけ試せる（`print(judge("グー", "チョキ"))` → `win`）

という良いことがあります。`return` で返した値が、呼んだ側に戻ってきます。

### 番号から手に変える：`HANDS[int(text) - 1]`

リストの番号は **0 から**始まります。プレイヤーは 1〜3 を打つので、1 を引いて 0〜2 にします。

| 入力 | `int(text) - 1` | `HANDS[...]` |
| --- | --- | --- |
| `"1"` | 0 | グー |
| `"2"` | 1 | チョキ |
| `"3"` | 2 | パー |

### 辞書を逆向きにする

サンプルでは「ある手に**勝つ**手」も必要なので、辞書を逆向きにしたものを作っています。

```python
BEATEN_BY = {loser: winner for winner, loser in WINS_AGAINST.items()}
# → {"チョキ": "グー", "パー": "チョキ", "グー": "パー"}
```

これは「辞書内包表記」という書き方で、次と同じ意味です。

```python
BEATEN_BY = {}
for winner, loser in WINS_AGAINST.items():
    BEATEN_BY[loser] = winner
```

### クセを読むしくみ

1. プレイヤーの手を `history` リストに毎回追加する
2. `history.count("グー")` のように、それぞれの手を何回出したか数える
3. いちばん多い手 `favorite` に勝つ手 `BEATEN_BY[favorite]` を出す

ただし毎回読むと強すぎてつまらないので、最初の3回と、3回に1回くらいはランダムにしています。
コンピューターの手は、**プレイヤーが選ぶ前に**決めています。後から決めるとズルになるからです。

## よくあるエラー

| 症状 | 原因と直し方 |
| --- | --- |
| `IndexError: list index out of range` | `HANDS[int(text)]` のように 1 を引き忘れています。または 4 などを入力しています |
| `KeyError: 'win'` | 結果の辞書のキーと、`judge()` が返す文字が一致していません（`"Win"` と `"win"` など） |
| 何を出しても「負け」になる | `judge()` の中で `player` と `computer` を逆に使っていないか確かめます |
| `ValueError: invalid literal for int()` | 数字以外を入力しました。サンプルのように `if text in ["1", "2", "3"]:` で先に確かめます |

## 練習問題のヒント

<details>
<summary>「直前に出した手のあとに何を出すか」まで読む</summary>

「グーのあとはパーを出しがち」のようなクセです。
`history` を前から順に見て、「直前の手がグーだったときに次に出した手」を数えます。

```python
after = [history[i + 1] for i in range(len(history) - 1) if history[i] == history[-1]]
```

`after` の中でいちばん多い手が、次に出しそうな手です。

</details>
