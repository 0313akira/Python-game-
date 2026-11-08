# 卓球部ストーリーメーカー

オーダー表のテキストから、インスタのストーリー用画像（1080×1920）を自動で作ります。
黒い角丸の枠・白文字・勝ちの「○」は赤丸、という部のいつものデザインです。

## 1. 画像を作る

```bash
pip install pillow
python make_story.py order.txt                       # story.png ができる
python make_story.py order.txt -b logo.png -o 2回戦.png  # 背景に部のロゴを薄く入れる
```

`order.txt` の書き方（空行で区切ったまとまりが、黒い枠 1 つになります）:

```
団体:一回戦

北陸大学vs富山大学B
○3-0

1.金澤3-0望月
2.中西3-0下清水
3.成川/守護3-0大滝/佐藤
4.田中 - 芝田
5.成川 - 佐藤
```

- 「○」は赤丸、「×」は青いバツで描かれます
- 文字の大きさは、一番長い行が画面に収まるように自動で決まります（`--size 80` で固定も可）
- 試合が進んだら `order.txt` の結果を書き換えて、もう一度実行するだけです

## 2. ストーリーに投稿する（任意）

Instagram の公式 API（Graph API）でストーリー投稿ができます。ただし条件があります。

1. 部のアカウントを **プロアカウント（ビジネス or クリエイター）** に切り替える（無料・設定から数分）
2. Meta for Developers でアプリを作り、`instagram_content_publish` 権限のアクセストークンと IG ユーザー ID を取得
3. 画像を **公開 URL** に置く（API はファイルを直接受け取れず、URL からしか読み込まない）

```bash
export IG_USER_ID=1784xxxxxxxxxxxx
export IG_ACCESS_TOKEN=EAAB....
python publish_story.py https://example.com/story.png
```

注意: API からの投稿では、スタンプ・メンション・リンクなどストーリー独自の装飾は付けられません。
アクセストークンは他人に見せたり、GitHub にコミットしたりしないでください。

## Web 版（写真から自動で作る）

`web/index.html` は claude.ai のアーティファクトとして公開しているページです。
オーダー用紙の写真を選ぶと Claude が名前を読み取り、スコアを選ぶだけでストーリー画像を作って保存できます。

### 誰でも使えるようにする

- **claude.ai 版**（写真の読み取りあり）: アーティファクトの「Share」から公開リンクを作る。読み取りは開いた人の Claude アカウントで行われる。
- **GitHub Pages 版**（ログイン不要・名前は手入力）: Settings → Pages → Source を「GitHub Actions」にすると、
  `.github/workflows/story-maker-pages.yml` が `https://0313akira.github.io/Python-game-/` に公開する。
  iPhone では「画像を保存」から共有メニューを開き、そのままインスタに送れる。

## リール動画テンプレート（`web/reel.html`）

フィード投稿（リール）用。試合の動画を選び、選手名・見出しを入れると、上に「選手 vs 選手」と見出し、
真ん中にプレー動画、下にチーム名の帯が付いた 1080×1920 の動画を書き出す。
使う範囲（はじめ・おわり）とズームを選べる。書き出しは再生しながら録画するので、動画の長さと同じだけ時間がかかる。
GitHub Pages では `https://0313akira.github.io/Python-game-/reel.html` に公開される。
