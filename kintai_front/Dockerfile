# Node.js の公式イメージを利用（例：Node 16）
FROM node:20.18.2

# 作業ディレクトリを設定
WORKDIR /app

# package.json を先にコピーして依存関係をインストール（キャッシュ利用のため）
COPY package.json /app/
RUN npm install

# 残りのソースコードをコピー
COPY . /app
