# 第6週の成果物：ハイスコア付き数当てゲーム
# 使う知識：ファイルの読み書き、モジュール（random, pathlib）
#
# 第4週の数当てゲームに「最少回数の記録」を足したもの。
# 記録は highscore.txt というファイルに保存されるので、
# プログラムを閉じても次に遊ぶときに残っている。

import random
from pathlib import Path

# このファイルと同じフォルダに highscore.txt を作る
SCORE_FILE = Path(__file__).parent / "highscore.txt"


def load_highscore():
    """保存されている記録を読む。まだなければ None を返す。"""
    if not SCORE_FILE.exists():
        return None
    text = SCORE_FILE.read_text(encoding="utf-8").strip()
    if not text.isdigit():
        return None
    return int(text)


def save_highscore(score):
    """記録をファイルに書き込む。"""
    SCORE_FILE.write_text(str(score), encoding="utf-8")


def play():
    """1回ゲームを遊び、かかった回数を返す。"""
    answer = random.randint(1, 100)
    count = 0
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
    best = load_highscore()
    if best is None:
        print("まだ記録はありません。")
    else:
        print(f"今の記録: {best} 回")

    print("1〜100 の数を当ててね！")
    count = play()

    if best is None or count < best:
        print("新記録！ 記録を保存しました。")
        save_highscore(count)
    else:
        print(f"記録は {best} 回のままです。")


main()
