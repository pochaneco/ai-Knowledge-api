/**
 * ルートヘルパー関数
 * Laravel風のroute()関数の代替
 */

// ルート定義
const routes = {
  // Auth routes
  "auth.login": "/auth/login",
  "auth.register": "/auth/register",
  "auth.logout": "/auth/logout",
  "auth.google": "/auth/google",

  // Project routes
  "project.index": "/projects",
  "project.create": "/projects/create",
  "project.store": "/api/v1/projects",
  "project.detail": (id) => `/projects/${id}`,
  "project.edit": (id) => `/projects/${id}/edit`,
  "project.members": (id) => `/projects/${id}/members`,
  "projects.destroy": (id) => `/api/v1/projects/${id}`,
  "projects.edit": (id) => `/projects/${id}/edit`,
  "projects.members.invite": (id) => `/projects/${id}/members/invite`,

  // Knowledge routes
  "knowledge.index": "/knowledge",
  "knowledge.create": "/knowledge/create",
  "knowledge.store": "/api/v1/knowledge",
  "knowledge.detail": (id) => `/knowledge/${id}`,
  "knowledge.show": (id) => `/knowledge/${id}`,
  "knowledge.edit": (id) => `/knowledge/${id}/edit`,
  "knowledge.search": "/knowledge/search",
  "knowledge.destroy": (id) => `/api/v1/knowledge/${id}`,
};

/**
 * ルート名からURLを生成
 * @param {string} name - ルート名
 * @param {*} params - パラメータ（オブジェクトまたは値）
 * @returns {string} URL
 */
export function route(name, params = null) {
  const routeDefinition = routes[name];

  if (!routeDefinition) {
    console.warn(`Route "${name}" not found`);
    return "/";
  }

  if (typeof routeDefinition === "function") {
    if (typeof params === "object" && params !== null) {
      // オブジェクトの場合、最初の値を使用
      const values = Object.values(params);
      return routeDefinition(values[0]);
    }
    return routeDefinition(params);
  }

  return routeDefinition;
}

// デフォルトエクスポート
export default route;
