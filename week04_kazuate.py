# 第4週の成果物：数当てゲーム
# 使う知識：変数、if、while、random、辞書
#
# コンピューターが決めた数を当てるゲーム。
# 難易度を選ぶと、数の範囲と挑戦できる回数が変わる。
# 回数を使い切ったら負け。

import random

# 難易度ごとの設定：番号 → (名前, いちばん大きい数, 挑戦できる回数)
LEVELS = {
    "1": ("かんたん", 10, 4),
    "2": ("ふつう", 100, 8),
    "3": ("むずかしい", 1000, 12),
}

print("難易度を選んでね。")
for key, (name, maximum, tries) in LEVELS.items():
    print(f"  {key}: {name}（1〜{maximum}、{tries} 回まで）")

choice = input("番号: ")
while choice not in LEVELS:
    choice = input("1, 2, 3 のどれかを入力してね: ")

name, maximum, tries = LEVELS[choice]
answer = random.randint(1, maximum)  # 正解の数
count = 0                            # 何回目の挑戦か

print(f"\n1〜{maximum} の数を当ててね！ チャンスは {tries} 回。")

while count < tries:
    text = input(f"[残り {tries - count} 回] 数を入力してください: ")

    # 数字以外が入力されたら、回数を減らさずにもう一度聞く
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
        print(f"正解！ 答えは {answer} でした。{count} 回で当たりました。")
        break
else:
    # while の条件が False になって終わったとき（＝回数を使い切ったとき）だけここに来る
    print(f"残念！ 答えは {answer} でした。")
