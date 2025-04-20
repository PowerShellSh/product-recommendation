FROM node:18-alpine AS builder

WORKDIR /app

# 依存関係ファイルをコピー
COPY package.json yarn.lock ./

# 依存関係をインストール
RUN yarn install --frozen-lockfile

# ソースコードをコピー
COPY . .

# ビルド
RUN yarn build

# 本番用イメージ
FROM node:18-alpine AS runner

WORKDIR /app

# 必要なファイルのみをコピー
# COPY --from=builder /app/next.config.js ./
# COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# ポートを公開
EXPOSE 3000

# アプリケーションを起動
CMD ["node", "server.js"] 