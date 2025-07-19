# Vidays - Copilot Instructions

## Architecture Overview

This is a **modular Flask application** with SQLAlchemy ORM for AI knowledge management. The architecture follows Flask blueprints pattern with clear separation of concerns:

- **Application Factory**: `app/__init__.py` creates the Flask app with `create_app()` function
- **Configuration**: Environment-based configs in `app/config.py` (development/production/testing)
- **Extensions**: Centralized initialization in `app/extensions.py` (SQLAlchemy, Flask-Login, OAuth, etc.)
- **Models**: SQLAlchemy models in `app/models/` with proper relationships and indexes
- **API Layer**: RESTful APIs in `app/api/v1/` with JSON responses
- **Services**: Business logic in `app/*/services.py` files
- **Views**: Web UI blueprints in `app/*/views.py` files

## Key Components

### Database Models (`app/models/`)
- **User**: Authentication with both password and Google OAuth support
- **Project**: Multi-tenant projects with membership roles (owner/admin/member)
- **KnowledgeBase**: Knowledge items linked to projects
- **SearchLog**: Search history tracking
- **ProjectInvitation**: Email-based project invitations

### Authentication Flow
- Dual auth: password-based (`User.set_password()`) and Google OAuth
- Flask-Login integration with `@login_required` decorator
- Custom permission decorator: `@require_project_permission('member|admin|owner')`

### API Structure
- All APIs under `/api/v1/` prefix
- JSON request/response format
- Consistent error handling with proper HTTP status codes
- Example: `POST /api/v1/auth/register` for user registration

## Development Workflow

### Environment Setup
```bash
# Use the provided scripts - they handle environment switching
./scripts/setup_env.sh local|production  # Sets up environment files
./scripts/run_app.sh local|production    # Starts the application
```

### Database Operations
```bash
# Flask-Migrate is configured - use these commands:
flask db migrate -m "Description"  # Generate migration
flask db upgrade                   # Apply migrations
flask db current                   # Check current state
```

### Testing
- Test configuration uses SQLite in-memory database
- Fixtures in `tests/conftest.py` provide test app and client
- Run tests with: `pytest tests/`

## Project-Specific Patterns

### Configuration Pattern
Environment-specific configs load different `.env` files:
- Development: `.env.local`
- Production: `.env.production`
- Testing: in-memory SQLite

### Service Layer Pattern
Business logic is separated into service modules:
- `app/auth/services.py` - Authentication operations
- `app/projects/services.py` - Project management
- `app/knowledge/services.py` - Knowledge base operations

### Error Handling
- Services raise `SQLAlchemyError` for database issues
- API endpoints return consistent JSON error responses
- Logging via `app/utils/logger.py`

### Blueprint Organization
Each major feature has both API and view blueprints:
- `app/auth/routes.py` - Web routes
- `app/api/v1/auth_api.py` - API endpoints

## Critical Files to Understand

- `app/__init__.py` - Application factory and blueprint registration
- `app/config.py` - Environment-based configuration system
- `app/extensions.py` - Flask extensions initialization
- `app/models/__init__.py` - Database models imports
- `app/utils/decorators.py` - Custom authentication/permission decorators

## Development Commands

```bash
# Start development server
./scripts/run_app.sh local

# Database initialization with sample data
curl http://localhost:5000/init-db

# Run tests
pytest tests/

# Docker development
docker-compose up -d
```

## Database Relationships

- **Users** ↔ **Projects** (many-to-many via `project_members` table)
- **Projects** → **KnowledgeBase** (one-to-many)
- **Projects** → **ProjectInvitation** (one-to-many)
- **Users** → **SearchLog** (one-to-many)

## Security Notes

- Passwords hashed with bcrypt
- Google OAuth integration via Authlib
- Email verification system implemented
- Project-based access control with role permissions
- Environment variables for sensitive data (`.env.*` files)

## 開発環境メモ

- VSCodeとテストコードの実行には`.venv`を使用しています。
- ブラウザでの動作確認はDocker経由で行っています。
