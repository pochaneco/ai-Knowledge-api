FROM python:3.8-slim

# 作業ディレクトリを設定
WORKDIR /app

# Node.js 18.xをインストール
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    default-mysql-client \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Node.jsの依存関係をコピーしてインストール
COPY package*.json ./
RUN npm install

# アプリケーションファイルをコピー
COPY . .

# 権限設定
RUN chmod +x scripts/*.sh

# フロントエンドをビルド
RUN npm run build

# ポート5000とViteポート（開発用）を公開
EXPOSE 5000 5173

# アプリケーションを起動
CMD ["python", "app.py"]
