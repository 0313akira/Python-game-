# 第5週の成果物：じゃんけんゲーム（クセを読むコンピューター）
# 使う知識：関数、リスト、辞書
#
# コンピューターと10回勝負する。
# コンピューターはあなたが今までに出した手を覚えていて、
# よく出す手に勝てる手を出してくる。同じ手ばかり出すと負けやすくなる。

import random

HANDS = ["グー", "チョキ", "パー"]

# どの手がどの手に勝つか（キーの手が、値の手に勝つ）
WINS_AGAINST = {
    "グー": "チョキ",
    "チョキ": "パー",
    "パー": "グー",
}

# ある手に勝つ手（WINS_AGAINST の逆）：例）グーに勝つのはパー
BEATEN_BY = {loser: winner for winner, loser in WINS_AGAINST.items()}


def ask_player_hand():
    """プレイヤーに手を選んでもらい、その手を返す。"""
    while True:
        text = input("1: グー  2: チョキ  3: パー  → ")
        if text in ["1", "2", "3"]:
            return HANDS[int(text) - 1]
        print("1, 2, 3 のどれかを入力してね。")


def computer_hand(history):
    """これまでのプレイヤーの手 history を見て、コンピューターの手を決める。"""
    # 最初の3回と、3回に1回くらいはランダム（読まれすぎないように）
    if len(history) < 3 or random.random() < 0.3:
        return random.choice(HANDS)

    # プレイヤーがいちばん多く出した手を数える
    counts = {hand: history.count(hand) for hand in HANDS}
    favorite = max(counts, key=counts.get)

    # その手に勝つ手を出す
    return BEATEN_BY[favorite]


def judge(player, computer):
    """勝ち負けを判定して "win" / "lose" / "draw" のどれかを返す。"""
    if player == computer:
        return "draw"
    if WINS_AGAINST[player] == computer:
        return "win"
    return "lose"


def show_habit(history):
    """最後に、プレイヤーがどの手を何回出したかを表示する。"""
    print("\nあなたのクセ:")
    for hand in HANDS:
        print(f"  {hand}: {history.count(hand)} 回")


def main():
    rounds = 10
    results = {"win": 0, "lose": 0, "draw": 0}
    history = []  # プレイヤーが出した手を順に記録する

    print("コンピューターは、あなたのクセを読んでくるよ。")

    for i in range(1, rounds + 1):
        print(f"\n--- {i} 回戦 ---")
        computer = computer_hand(history)  # 先にコンピューターが決める（ズルなし）
        player = ask_player_hand()
        history.append(player)
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
    show_habit(history)


main()
