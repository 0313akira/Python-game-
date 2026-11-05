# 第7週の成果物：文字バトルゲーム（勇者 vs モンスター）
# 使う知識：クラスとオブジェクト、継承
#
# 勇者を操作して、モンスターを3体倒せばクリア。
#   攻撃 … ふつうの攻撃
#   魔法 … MP を 8 使う強い攻撃
#   回復 … 回復薬で HP を回復（3個まで）
# モンスターを倒すとレベルが上がって強くなる。
# モンスターはそれぞれ特技を持っている。ドラゴンが息を吸いこんだら要注意！

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

    def roll_damage(self, power):
        """power の 80%〜120% のダメージを決める。"""
        return random.randint(power * 8 // 10, power * 12 // 10)

    def hit(self, target):
        damage = self.roll_damage(self.attack)
        target.take_damage(damage)
        print(f"{self.name} の攻撃！ {target.name} に {damage} のダメージ。")

    def status(self):
        return f"{self.name} HP {self.hp}/{self.max_hp}"


class Hero(Character):
    """勇者。Character の機能に加えて、魔法・回復・レベルアップができる。"""

    MAGIC_COST = 8

    def __init__(self, name):
        super().__init__(name, hp=50, attack=10)
        self.level = 1
        self.max_mp = 16
        self.mp = self.max_mp
        self.potions = 3

    def status(self):
        return (f"{self.name} Lv{self.level}  HP {self.hp}/{self.max_hp}"
                f"  MP {self.mp}/{self.max_mp}  回復薬 {self.potions}")

    def magic(self, target):
        if self.mp < self.MAGIC_COST:
            print("MP が足りない！")
            return False
        self.mp -= self.MAGIC_COST
        damage = self.roll_damage(self.attack * 2)
        target.take_damage(damage)
        print(f"{self.name} は魔法をとなえた！ {target.name} に {damage} の大ダメージ！")
        return True

    def heal(self):
        if self.potions == 0:
            print("回復薬がもうない！")
            return False
        self.potions -= 1
        before = self.hp
        self.hp = min(self.max_hp, self.hp + 30)
        print(f"{self.name} は回復薬を使った。HP が {self.hp - before} 回復した！")
        return True

    def level_up(self):
        self.level += 1
        self.max_hp += 12
        self.attack += 3
        self.max_mp += 4
        self.hp = min(self.max_hp, self.hp + 20)  # 少しだけ回復
        self.mp = self.max_mp                     # MP は全回復
        print(f"\n{self.name} はレベル {self.level} になった！")
        print(f"  最大HP {self.max_hp} / 攻撃力 {self.attack} / 最大MP {self.max_mp}")


class Monster(Character):
    """モンスターの共通部分。special_rate の確率で特技を使う。"""

    special_rate = 0.0

    def act(self, hero):
        if random.random() < self.special_rate:
            self.special(hero)
        else:
            self.hit(hero)

    def special(self, hero):
        self.hit(hero)  # 特技がないモンスターはふつうに攻撃


class Slime(Monster):
    special_rate = 0.3

    def __init__(self):
        super().__init__("スライム", hp=22, attack=5)

    def special(self, hero):
        before = self.hp
        self.hp = min(self.max_hp, self.hp + 8)
        print(f"{self.name} はぷるぷるふるえた。HP が {self.hp - before} 回復した！")


class Goblin(Monster):
    special_rate = 0.3

    def __init__(self):
        super().__init__("ゴブリン", hp=45, attack=9)

    def special(self, hero):
        print(f"{self.name} のれんぞく攻撃！")
        self.hit(hero)
        self.hit(hero)


class Dragon(Monster):
    """ドラゴンは「息を吸いこむ」→ 次のターンに「ほのお」を吐く。"""

    special_rate = 0.35

    def __init__(self):
        super().__init__("ドラゴン", hp=130, attack=15)
        self.charging = False

    def act(self, hero):
        if self.charging:
            self.charging = False
            damage = self.roll_damage(34)
            hero.take_damage(damage)
            print(f"{self.name} はほのおを吐いた！ {hero.name} に {damage} の大ダメージ！")
        elif random.random() < self.special_rate:
            self.charging = True
            print(f"{self.name} は大きく息を吸いこんだ…！（次のターンに注意）")
        else:
            self.hit(hero)


def choose_action(hero):
    while True:
        text = input(f"1: 攻撃  2: 魔法（MP{Hero.MAGIC_COST}）  3: 回復  → ")
        if text in ["1", "2", "3"]:
            return text
        print("1, 2, 3 のどれかを入力してね。")


def battle(hero, monster):
    """1体のモンスターと戦う。勇者が勝てば True を返す。"""
    print(f"\n{monster.name} があらわれた！")
    while hero.is_alive() and monster.is_alive():
        print(f"\n[{hero.status()}]")
        print(f"[{monster.status()}]")
        action = choose_action(hero)
        if action == "1":
            hero.hit(monster)
        elif action == "2":
            if not hero.magic(monster):
                continue  # 使えなかったら、もう一度選び直す
        else:
            if not hero.heal():
                continue

        if monster.is_alive():
            monster.act(hero)

    if hero.is_alive():
        print(f"{monster.name} をたおした！")
        return True
    print(f"{hero.name} はたおれてしまった…")
    return False


def main():
    name = input("勇者の名前を入力してください: ") or "勇者"
    hero = Hero(name)
    monsters = [Slime(), Goblin(), Dragon()]

    for monster in monsters:
        if not battle(hero, monster):
            print("\nゲームオーバー")
            return
        if monster is not monsters[-1]:
            hero.level_up()

    print(f"\nおめでとう！ {hero.name} はすべてのモンスターをたおした！")


main()
