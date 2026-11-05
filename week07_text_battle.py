# 第7週の成果物：文字バトルゲーム（勇者 vs モンスター）
# 使う知識：クラスとオブジェクト
#
# 勇者を操作して、モンスターを3体倒せばクリア。
# 勇者もモンスターも Character クラスから作る。

import random


class Character:
    """勇者とモンスターに共通する「キャラクター」の設計図。"""

    def __init__(self, name, hp, attack):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def hit(self, target):
        """target を攻撃する。ダメージは攻撃力の 80%〜120% でばらつく。"""
        damage = random.randint(self.attack * 8 // 10, self.attack * 12 // 10)
        target.take_damage(damage)
        print(f"{self.name} の攻撃！ {target.name} に {damage} のダメージ。")

    def status(self):
        return f"{self.name} HP {self.hp}/{self.max_hp}"


class Hero(Character):
    """勇者。Character の機能に加えて、回復ができる。"""

    def __init__(self, name):
        super().__init__(name, hp=60, attack=12)
        self.potions = 3  # 回復薬の数

    def heal(self):
        if self.potions == 0:
            print("回復薬がもうない！")
            return False
        self.potions = self.potions - 1
        amount = 25
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} は回復薬を使った。HP が回復した！（残り {self.potions} 個）")
        return True


def choose_action():
    while True:
        text = input("1: 攻撃  2: 回復  → ")
        if text in ["1", "2"]:
            return text
        print("1 か 2 を入力してね。")


def battle(hero, monster):
    """1体のモンスターと戦う。勇者が勝てば True を返す。"""
    print(f"\n{monster.name} があらわれた！")
    while hero.is_alive() and monster.is_alive():
        print(f"\n[{hero.status()}]  [{monster.status()}]")
        action = choose_action()
        if action == "1":
            hero.hit(monster)
        else:
            if not hero.heal():
                continue  # 回復できなかったら、もう一度選び直す

        if monster.is_alive():
            monster.hit(hero)

    if hero.is_alive():
        print(f"{monster.name} をたおした！")
        return True
    print(f"{hero.name} はたおれてしまった…")
    return False


def main():
    name = input("勇者の名前を入力してください: ") or "勇者"
    hero = Hero(name)
    monsters = [
        Character("スライム", hp=20, attack=5),
        Character("ゴブリン", hp=35, attack=8),
        Character("ドラゴン", hp=60, attack=12),
    ]

    for monster in monsters:
        if not battle(hero, monster):
            print("\nゲームオーバー")
            return

    print(f"\nおめでとう！ {hero.name} はすべてのモンスターをたおした！")


main()
