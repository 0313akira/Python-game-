# 第7週 文字バトルゲーム：ヒントと解説

サンプル: [`week07_text_battle.py`](../week07_text_battle.py)

## 作るもの

勇者とモンスターが交代で攻撃し合い、どちらかの HP が 0 になったら終わり。

```
スライム があらわれた！

[勇者 HP 50/50]
[スライム HP 22/22]
1: 攻撃  2: 魔法  3: 回復  → 1
勇者 の攻撃！ スライム に 11 のダメージ。
スライム の攻撃！ 勇者 に 5 のダメージ。
```

まずは「勇者 vs スライム1体、攻撃だけ」の基本版を作りましょう。
魔法・回復・レベルアップ・特技は、1つずつ足していきます。

## ヒント

<details>
<summary>ヒント1：クラスで何を表すか</summary>

勇者もモンスターも「名前・HP・攻撃力を持ち、攻撃できる」ので、同じ設計図（クラス）で作れます。

- 持っているデータ（属性）: `name`, `hp`, `attack`
- できること（メソッド）: `hit(target)`（相手を攻撃）、`is_alive()`（生きているか）

</details>

<details>
<summary>ヒント2：クラスの形</summary>

```python
class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def hit(self, target):
        target.hp = target.hp - self.attack
        print(f"{self.name} の攻撃！ {target.name} に {self.attack} のダメージ。")


hero = Character("勇者", 50, 10)
slime = Character("スライム", 22, 5)
```

あとは `while hero.is_alive() and slime.is_alive():` の中で交互に `hit` します。

</details>

<details>
<summary>ヒント3：ほぼ答え（戦いのループ）</summary>

```python
while hero.is_alive() and slime.is_alive():
    input("Enter で攻撃 → ")
    hero.hit(slime)
    if slime.is_alive():      # 倒したあとに反撃されないように
        slime.hit(hero)

if hero.is_alive():
    print("スライムをたおした！")
else:
    print("ゲームオーバー")
```

</details>

## 解説

### `__init__` と `self`

- `__init__` は、`Character("勇者", 50, 10)` のように**作った瞬間に動く**特別なメソッドです。
- `self` は「このキャラクター自身」です。`self.hp` は「自分の HP」。

`hero.hit(slime)` と呼ぶと、`hit` の中では `self` が `hero`、`target` が `slime` になります。

### 継承：`class Hero(Character):`

勇者だけが持つ機能（魔法、回復、レベルアップ）は、`Character` を**引き継いだ**クラスに書きます。

```python
class Hero(Character):
    def __init__(self, name):
        super().__init__(name, hp=50, attack=10)   # 親（Character）の準備をしてもらう
        self.mp = 16                               # 勇者だけが持つもの
```

- `Hero` は `Character` の `hit` や `is_alive` をそのまま使えます。
- `super().__init__(...)` は「親クラスの `__init__` を呼ぶ」という意味です。これを忘れると `self.hp` などが作られません。

### メソッドの上書き（オーバーライド）

`Monster` には `act()`（自分のターンの行動）があり、ふだんは「たまに特技、それ以外は攻撃」です。
`Dragon` は同じ名前の `act()` を自分で書き直して、「息を吸いこむ → 次のターンにほのお」という動きにしています。

呼ぶ側は相手がだれでも `monster.act(hero)` と書くだけで、モンスターごとに違う動きになります。
これがクラスを使ういちばんの便利さです。

### ダメージにばらつきを付ける

```python
random.randint(power * 8 // 10, power * 12 // 10)
```

攻撃力の 80%〜120% の範囲でランダムにしています。`//` は「割って小数を切り捨てる」計算です
（`randint` は整数しか受け取れないため）。

### 回復できなかったら選び直し

`heal()` と `magic()` は、使えたら `True`、使えなかったら `False` を返します。
`False` のときは `continue` でループの先頭に戻り、モンスターのターンにしません。

## よくあるエラー

| 症状 | 原因と直し方 |
| --- | --- |
| `TypeError: __init__() missing 1 required positional argument` | クラスを作るときの引数が足りません。`Character("勇者", 50, 10)` のように全部渡します |
| `AttributeError: 'Hero' object has no attribute 'hp'` | `Hero` の `__init__` で `super().__init__(...)` を呼び忘れています |
| `NameError: name 'hp' is not defined` | メソッドの中で `self.` を付け忘れています。`hp` ではなく `self.hp` |
| `TypeError: hit() takes 1 positional argument but 2 were given` | メソッドの最初の引数 `self` を書き忘れています。`def hit(self, target):` |
| HP がマイナスになる | `max(0, self.hp - amount)` のように、0 より下にならないようにします |

## 練習問題のヒント

<details>
<summary>宝箱（回復薬が増える）を追加する</summary>

モンスターを倒したあと（`level_up()` を呼んでいるあたり）で、
`if random.random() < 0.5:` のように確率で `hero.potions += 1` します。

</details>

<details>
<summary>逃げるコマンドを追加する</summary>

`choose_action()` に `4: 逃げる` を足し、`battle()` の中で選ばれたら確率で成功させます。
逃げたら戦いを終えたいので、`battle()` が「勝ち・負け・逃げた」の3種類を返せるようにする必要があります。
`True` / `False` の代わりに、`"win"` / `"lose"` / `"run"` の文字を返す形に変えるのがおすすめです。

</details>
