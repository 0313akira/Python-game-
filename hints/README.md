# ヒントと解説

課題で詰まったときに読むページです。

| 週 | 課題 | ヒントと解説 |
| --- | --- | --- |
| 4 | 数当てゲーム | [week04_kazuate.md](week04_kazuate.md) |
| 5 | じゃんけんゲーム | [week05_janken.md](week05_janken.md) |
| 6 | ランキング付き数当て | [week06_ranking.md](week06_ranking.md) |
| 7 | 文字バトルゲーム | [week07_text_battle.md](week07_text_battle.md) |
| 8〜10 | よけゲーム（Pygame） | [week10_yoke_game.md](week10_yoke_game.md) |

## このページの使い方

各ページは次の順に並んでいます。上から順に、必要なところまでだけ読んでください。

1. **作るもの**: 完成したらどう動くか
2. **ヒント**: 3段階あり、クリックすると開きます。ヒント1で書けたら、ヒント2は開かなくてOK
3. **解説**: サンプルコードの大事なところの説明。完成したあとに読む
4. **よくあるエラー**: エラーが出たときに見る

## 詰まったときの手順

1. **エラーメッセージの最後の行を読む**。何が起きたかはそこに書いてあります。
2. **その1行上の `line 〇〇` を見る**。エラーが起きた行の番号です。
3. **`print()` で中身を確かめる**。「この変数には何が入っているはず」と思ったら、実際に表示してみます。
   ```python
   print("guess の中身:", guess, type(guess))
   ```
4. **15分考えても進まなければ、ヒントを開く**。悩む時間も勉強ですが、止まりすぎるのはもったいないです。
5. **答えを見たら、閉じてからもう一度自分で書く**。見ながら写すだけでは身につきません。

## よく見るエラー早見表

| エラー | 意味 | よくある原因 |
| --- | --- | --- |
| `SyntaxError: invalid syntax` | 書き方が Python のルールに合っていない | `:` の付け忘れ、カッコの閉じ忘れ、全角文字（`（` や全角スペース） |
| `IndentationError` | 字下げ（インデント）がおかしい | スペースの数がそろっていない、`if` のあとの行を字下げしていない |
| `NameError: name 'x' is not defined` | その名前の変数・関数がない | 書き間違い（`anser` と `answer`）、使う前に作っていない |
| `TypeError: '<' not supported between instances of 'str' and 'int'` | 文字と数を比べようとした | `input()` の結果を `int()` で数にし忘れた |
| `ValueError: invalid literal for int()` | 数にできない文字を `int()` に渡した | 入力に数字以外が入っていた |
| `IndexError: list index out of range` | リストにない番号を指定した | 番号は 0 から始まる。3つのリストの最後は `[2]` |
| `KeyError` | 辞書にないキーを指定した | キーの書き間違い、`"1"`（文字）と `1`（数）の違い |
| `AttributeError: 'X' object has no attribute 'y'` | そのオブジェクトにその属性・メソッドがない | `self.` の付け忘れ、書き間違い |
| `ModuleNotFoundError: No module named 'pygame'` | ライブラリが入っていない | `pip install pygame` をしていない |
