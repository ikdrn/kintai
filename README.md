<!-- ファイル: README.md -->

# 勤怠管理システム

## 概要
本プロジェクトは、Vue.js と Django を利用した勤怠管理システムです。

## 環境変数の設定
コマンドプロンプトのsetで値を事前にセットしておく。

```dotenv
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
KINTAI_DB_NAME
KINTAI_DB_USER
KINTAI_DB_PASSWORD
KINTAI_DB_HOST
KINTAI_DB_PORT
DJANGO_CORS_ALLOWED_ORIGINS

#起動
docker-compose build --no-cache
docker-compose up

#変更内容の確認
git status
変更ファイルのステージング

全ての変更をステージする
git add .

コミットの作成.変更内容を説明するメッセージを付けてコミットします:
git commit -m "更新内容の説明"
リモートリポジトリへのプッシュ
既にリモートリポジトリを設定している場合は、以下のコマンドで更新内容を反映します: