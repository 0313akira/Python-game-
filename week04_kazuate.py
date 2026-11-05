# 第4週の成果物：数当てゲーム
# 使う知識：変数、if、while、random
#
# コンピューターが 1〜100 の数を1つ決めるので、それを当てるゲーム。

import random

answer = random.randint(1, 100)  # 正解の数
count = 0                        # 何回目の挑戦か

print("1〜100 の数を当ててね！")

while True:
    text = input("数を入力してください: ")

    # 数字以外が入力されたら、もう一度聞く
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
