# 第5週の成果物：じゃんけんゲーム
# 使う知識：関数、リスト、辞書
#
# コンピューターと5回勝負して、勝った回数を数える。

import random

HANDS = ["グー", "チョキ", "パー"]

# どの手がどの手に勝つか（キーの手が、値の手に勝つ）
WINS_AGAINST = {
    "グー": "チョキ",
    "チョキ": "パー",
    "パー": "グー",
}


def ask_player_hand():
    """プレイヤーに手を選んでもらい、その手を返す。"""
    while True:
        text = input("1: グー  2: チョキ  3: パー  → ")
        if text in ["1", "2", "3"]:
            return HANDS[int(text) - 1]
        print("1, 2, 3 のどれかを入力してね。")


def judge(player, computer):
    """勝ち負けを判定して "win" / "lose" / "draw" のどれかを返す。"""
    if player == computer:
        return "draw"
    if WINS_AGAINST[player] == computer:
        return "win"
    return "lose"


def main():
    rounds = 5
    results = {"win": 0, "lose": 0, "draw": 0}

    for i in range(1, rounds + 1):
        print(f"\n--- {i} 回戦 ---")
        player = ask_player_hand()
        computer = random.choice(HANDS)
        print(f"あなた: {player}  コンピューター: {computer}")

        result = judge(player, computer)
        results[result] = results[result] + 1

        if result == "win":
            print("あなたの勝ち！")
        elif result == "lose":
            print("あなたの負け…")
        else:
            print("あいこ。")

    print(f"\n結果: {results['win']} 勝 {results['lose']} 敗 {results['draw']} 分け")


main()
