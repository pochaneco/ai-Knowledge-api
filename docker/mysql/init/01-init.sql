-- MySQL初期化スクリプト
-- UTF8MB4設定とタイムゾーン設定

SET NAMES utf8mb4;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_database = utf8mb4;
SET character_set_results = utf8mb4;
SET character_set_server = utf8mb4;

-- タイムゾーンをアジア/東京に設定
SET time_zone = '+09:00';

-- ユーザーに適切な権限を付与
GRANT ALL PRIVILEGES ON ai_knowledge_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
