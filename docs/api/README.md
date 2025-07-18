# API仕様

AI Knowledge API v1の詳細な仕様書です。

## 🌐 ベースURL

```
開発環境: http://localhost:5000/api/v1
本番環境: https://your-domain.com/api/v1
```

## 🔑 認証

### 認証方式

1. **セッション認証**: Webアプリケーション用
2. **Google OAuth**: ソーシャルログイン

### レスポンス形式

成功時:
```json
{
  "status": "success",
  "data": { ... },
  "message": "操作が成功しました"
}
```

エラー時:
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": { ... }
  }
}
```

## 👤 認証API

### POST /auth/register

新規ユーザー登録

**リクエスト:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "ユーザー名"
}
```

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "ユーザー名",
      "created_at": "2024-01-01T00:00:00Z"
    }
  },
  "message": "ユーザー登録が完了しました"
}
```

### POST /auth/login

ログイン

**リクエスト:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "ユーザー名"
    }
  },
  "message": "ログインしました"
}
```

### POST /auth/logout

ログアウト

**レスポンス:**
```json
{
  "status": "success",
  "message": "ログアウトしました"
}
```

### GET /auth/me

現在のユーザー情報取得

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "ユーザー名",
      "created_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

## 📁 プロジェクトAPI

### GET /projects

プロジェクト一覧取得

**クエリパラメータ:**
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20）

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "projects": [
      {
        "id": 1,
        "name": "プロジェクト名",
        "description": "プロジェクトの説明",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "role": "owner"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 5,
      "pages": 1
    }
  }
}
```

### POST /projects

プロジェクト作成

**リクエスト:**
```json
{
  "name": "新しいプロジェクト",
  "description": "プロジェクトの説明"
}
```

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "project": {
      "id": 2,
      "name": "新しいプロジェクト",
      "description": "プロジェクトの説明",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "role": "owner"
    }
  },
  "message": "プロジェクトを作成しました"
}
```

### GET /projects/{id}

プロジェクト詳細取得

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "project": {
      "id": 1,
      "name": "プロジェクト名",
      "description": "プロジェクトの説明",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "role": "owner",
      "members": [
        {
          "id": 1,
          "name": "ユーザー名",
          "email": "user@example.com",
          "role": "owner"
        }
      ],
      "knowledge_count": 10
    }
  }
}
```

### PUT /projects/{id}

プロジェクト更新

**リクエスト:**
```json
{
  "name": "更新されたプロジェクト名",
  "description": "更新された説明"
}
```

### DELETE /projects/{id}

プロジェクト削除

**レスポンス:**
```json
{
  "status": "success",
  "message": "プロジェクトを削除しました"
}
```

## 👥 プロジェクトメンバーAPI

### GET /projects/{id}/members

メンバー一覧取得

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "members": [
      {
        "id": 1,
        "name": "ユーザー名",
        "email": "user@example.com",
        "role": "owner",
        "joined_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

### POST /projects/{id}/invite

メンバー招待

**リクエスト:**
```json
{
  "email": "newuser@example.com",
  "role": "member"
}
```

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "invitation": {
      "id": 1,
      "email": "newuser@example.com",
      "role": "member",
      "status": "pending",
      "created_at": "2024-01-01T00:00:00Z"
    }
  },
  "message": "招待メールを送信しました"
}
```

### PUT /projects/{id}/members/{user_id}

メンバーロール変更

**リクエスト:**
```json
{
  "role": "admin"
}
```

### DELETE /projects/{id}/members/{user_id}

メンバー削除

**レスポンス:**
```json
{
  "status": "success",
  "message": "メンバーを削除しました"
}
```

## 📚 ナレッジAPI

### GET /projects/{id}/knowledge

ナレッジ一覧取得

**クエリパラメータ:**
- `page`: ページ番号
- `per_page`: 1ページあたりの件数
- `search`: 検索キーワード
- `tags`: タグ（カンマ区切り）

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "knowledge": [
      {
        "id": 1,
        "title": "ナレッジタイトル",
        "content": "ナレッジの内容",
        "tags": ["tag1", "tag2"],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "author": {
          "id": 1,
          "name": "作成者名"
        }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 5,
      "pages": 1
    }
  }
}
```

### POST /projects/{id}/knowledge

ナレッジ作成

**リクエスト:**
```json
{
  "title": "新しいナレッジ",
  "content": "ナレッジの内容",
  "tags": ["tag1", "tag2"]
}
```

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "knowledge": {
      "id": 2,
      "title": "新しいナレッジ",
      "content": "ナレッジの内容",
      "tags": ["tag1", "tag2"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "author": {
        "id": 1,
        "name": "作成者名"
      }
    }
  },
  "message": "ナレッジを作成しました"
}
```

### GET /projects/{project_id}/knowledge/{id}

ナレッジ詳細取得

### PUT /projects/{project_id}/knowledge/{id}

ナレッジ更新

### DELETE /projects/{project_id}/knowledge/{id}

ナレッジ削除

## 🔍 検索API

### POST /search

全文検索

**リクエスト:**
```json
{
  "query": "検索キーワード",
  "project_ids": [1, 2],
  "filters": {
    "tags": ["tag1"],
    "date_from": "2024-01-01",
    "date_to": "2024-12-31"
  }
}
```

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "title": "マッチしたナレッジ",
        "content_snippet": "検索キーワードを含む内容の抜粋...",
        "project": {
          "id": 1,
          "name": "プロジェクト名"
        },
        "score": 0.95,
        "matched_fields": ["title", "content"]
      }
    ],
    "total": 1,
    "query_time": 0.02
  }
}
```

## 📊 統計API

### GET /projects/{id}/stats

プロジェクト統計

**レスポンス:**
```json
{
  "status": "success",
  "data": {
    "stats": {
      "knowledge_count": 25,
      "member_count": 5,
      "recent_activity": [
        {
          "type": "knowledge_created",
          "title": "新しいナレッジが作成されました",
          "user": "ユーザー名",
          "created_at": "2024-01-01T00:00:00Z"
        }
      ],
      "popular_tags": [
        {"tag": "Python", "count": 10},
        {"tag": "API", "count": 8}
      ]
    }
  }
}
```

## ❌ エラーコード

| コード | 説明 |
|--------|------|
| `INVALID_CREDENTIALS` | 認証情報が無効 |
| `PERMISSION_DENIED` | アクセス権限なし |
| `RESOURCE_NOT_FOUND` | リソースが見つからない |
| `VALIDATION_ERROR` | バリデーションエラー |
| `DUPLICATE_RESOURCE` | 重複リソース |
| `RATE_LIMIT_EXCEEDED` | レート制限超過 |
| `INTERNAL_ERROR` | 内部サーバーエラー |

## 📝 レート制限

- **認証API**: 10回/分
- **その他API**: 100回/分
- **検索API**: 30回/分

## 📅 APIバージョニング

現在のバージョン: `v1`

バージョンはURLパスで指定:
```
/api/v1/projects
```

## 🔧 SDKとツール

### curl例

```bash
# ログイン
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# プロジェクト一覧取得
curl -X GET http://localhost:5000/api/v1/projects \
  -H "Cookie: session=your_session_cookie"
```

### Python SDK例

```python
import requests

class AIKnowledgeAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, email, password):
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password}
        )
        return response.json()
    
    def get_projects(self):
        response = self.session.get(f"{self.base_url}/projects")
        return response.json()
```
