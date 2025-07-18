# ドキュメント一覧

AI Knowledge APIの包括的なドキュメントです。

## 📚 ドキュメント構成

### 🚀 セットアップガイド
各環境に応じたセットアップ方法を選択してください。

- **[Docker環境](setup/docker-setup.md)** - 推奨環境、すべてが自動化
- **[Python venv環境](setup/venv-setup.md)** - ローカル開発、詳細制御
- **[サーバー環境](setup/server-setup.md)** - 本番デプロイ、VPS・共用サーバー
- **[レガシー情報](setup/legacy-readme.md)** - 旧READMEの内容
- **[Docker詳細](setup/docker-detailed.md)** - Docker設定の詳細情報

### 💻 開発関連
開発に参加する際に必要な情報です。

- **[開発ガイド](development/README.md)** - 開発フロー、コーディング規約、環境ファイル設定
- **[認証システム](development/authentication.md)** - 認証の実装詳細

### 🏗️ アーキテクチャ
システムの構成と設計について説明します。

- **[システムアーキテクチャ](architecture/README.md)** - 全体設計、技術スタック
- **[プロジェクト構造](architecture/project-structure.md)** - ディレクトリ構成
- **[更新されたプロジェクト構造](architecture/updated-structure.md)** - 最新の構造情報

### 📡 API仕様
REST APIの詳細な仕様書です。

- **[API仕様書](api/README.md)** - エンドポイント、リクエスト・レスポンス形式

### 🔧 トラブルシューティング
よくある問題とその解決方法です。

- **[トラブルシューティング](troubleshooting.md)** - 問題解決ガイド

## 🎯 目的別ガイド

### 初めての方
1. [プロジェクト概要](../README.md) を読む
2. 環境に応じたセットアップガイドを選択
   - Docker推奨: [docker-setup.md](setup/docker-setup.md)
   - ローカル開発: [venv-setup.md](setup/venv-setup.md)
3. 動作確認とブラウザでのアクセス

### 開発者の方
1. [開発ガイド](development/README.md) を読む
2. [システムアーキテクチャ](architecture/README.md) を理解
3. [API仕様](api/README.md) を確認
4. 開発環境のセットアップ

### 運用・管理者の方
1. [サーバー環境セットアップ](setup/server-setup.md) を読む
2. [システムアーキテクチャ](architecture/README.md) を理解
3. [トラブルシューティング](troubleshooting.md) を確認

### API利用者の方
1. [API仕様書](api/README.md) を読む
2. 認証方法を確認
3. エンドポイントとレスポンス形式を理解

## 📋 更新履歴

- **2024-07-18**: ドキュメント構造の整理、各環境別セットアップガイドの分離
- **2024-01-01**: 初版リリース

## 🤝 ドキュメントの改善

ドキュメントの改善提案や誤りの報告は、以下の方法でお願いします：

1. **Issue報告**: GitHub Issuesで報告
2. **プルリクエスト**: 直接修正提案
3. **フィードバック**: 開発チームへの直接連絡

## 📞 サポート

技術的な質問やサポートが必要な場合：

- **GitHub Issues**: バグ報告・機能要望
- **Discussions**: 一般的な質問・相談
- **Email**: 緊急時・プライベートな問い合わせ
