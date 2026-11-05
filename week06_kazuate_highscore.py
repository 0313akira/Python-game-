# 第6週の成果物：ランキング付き数当てゲーム
# 使う知識：ファイルの読み書き、リスト、並べ替え、モジュール（random, pathlib）
#
# 第4週の数当てゲームに「上位5位までのランキング」を足したもの。
# ランキングは ranking.txt というファイルに保存されるので、
# プログラムを閉じても次に遊ぶときに残っている。
#
# ranking.txt の中身は 1 行に 1 人、「名前,回数」の形で書く。
#   例） あきら,6

import random
from pathlib import Path

# このファイルと同じフォルダに ranking.txt を作る
RANKING_FILE = Path(__file__).parent / "ranking.txt"
RANKING_SIZE = 5


def load_ranking():
    """保存されているランキングを [(名前, 回数), ...] のリストで返す。"""
    ranking = []
    if not RANKING_FILE.exists():
        return ranking
    for line in RANKING_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split(",")
        if len(parts) == 2 and parts[1].isdigit():  # 形のおかしい行は読み飛ばす
            ranking.append((parts[0], int(parts[1])))
    return ranking


def save_ranking(ranking):
    lines = [f"{name},{count}" for name, count in ranking]
    RANKING_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def show_ranking(ranking):
    print("\n=== ランキング（少ない回数ほど上）===")
    if not ranking:
        print("  まだ記録はありません。")
    for i, (name, count) in enumerate(ranking, start=1):
        print(f"  {i}位  {name}  {count} 回")
    print()


def play():
    """1回ゲームを遊び、かかった回数を返す。"""
    answer = random.randint(1, 100)
    count = 0
    print("1〜100 の数を当ててね！")
    while True:
        text = input("数を入力してください: ")
        if not text.isdigit():
            print("数字を入力してね。")
            continue
        guess = int(text)
        count = count + 1
        if guess < answer:
            print("もっと大きいよ。")
        elif guess > answer:
            print("もっと小さいよ。")
        else:
            print(f"正解！ {count} 回で当たりました。")
            return count


def main():
    ranking = load_ranking()
    show_ranking(ranking)

    count = play()

    # ランキングに入れるかどうか：5人未満か、5位より少ない回数なら入れる
    if len(ranking) < RANKING_SIZE or count < ranking[-1][1]:
        name = input("ランキング入り！ 名前を入力してください: ").strip() or "ななし"
        name = name.replace(",", "")  # カンマはファイルの区切りに使うので消す
        ranking.append((name, count))
        ranking.sort(key=lambda item: item[1])  # 回数の少ない順に並べる
        ranking = ranking[:RANKING_SIZE]        # 上位5人だけ残す
        save_ranking(ranking)
    else:
        print("今回はランキング入りならず。")

    show_ranking(ranking)


main()
