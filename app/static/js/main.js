// メインJavaScriptファイル

// ユーティリティ関数
const Utils = {
  // APIリクエストのヘルパー
  async apiRequest(url, options = {}) {
    const defaultOptions = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, mergedOptions);
      const data = await response.json();

      return { response, data };
    } catch (error) {
      console.error("API Request Error:", error);
      throw error;
    }
  },

  // 日付フォーマット
  formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString("ja-JP", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  },

  // エラーメッセージ表示
  showError(message) {
    const alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-danger alert-dismissible fade show";
    alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

    const container = document.querySelector(".container");
    container.insertBefore(alertDiv, container.firstChild);

    // 5秒後に自動で削除
    setTimeout(() => {
      if (alertDiv.parentNode) {
        alertDiv.remove();
      }
    }, 5000);
  },

  // 成功メッセージ表示
  showSuccess(message) {
    const alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-success alert-dismissible fade show";
    alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

    const container = document.querySelector(".container");
    container.insertBefore(alertDiv, container.firstChild);

    // 5秒後に自動で削除
    setTimeout(() => {
      if (alertDiv.parentNode) {
        alertDiv.remove();
      }
    }, 5000);
  },

  // ローディング表示
  showLoading(element) {
    element.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
            </div>
        `;
  },

  // 確認ダイアログ
  confirm(message) {
    return window.confirm(message);
  },
};

// 認証関連
const Auth = {
  // ログイン状態チェック
  async checkAuthStatus() {
    try {
      const { response, data } = await Utils.apiRequest("/api/v1/auth/me");
      return response.ok ? data.user : null;
    } catch (error) {
      return null;
    }
  },

  // ログアウト
  async logout() {
    try {
      const { response } = await Utils.apiRequest("/api/v1/auth/logout", {
        method: "POST",
      });

      if (response.ok) {
        window.location.href = "/auth/login";
      }
    } catch (error) {
      Utils.showError("ログアウトに失敗しました");
    }
  },
};

// プロジェクト関連
const Project = {
  // プロジェクト削除
  async delete(projectId) {
    if (!Utils.confirm("このプロジェクトを削除しますか？")) {
      return;
    }

    try {
      const { response, data } = await Utils.apiRequest(
        `/api/v1/projects/${projectId}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        Utils.showSuccess("プロジェクトが削除されました");
        setTimeout(() => {
          window.location.href = "/projects";
        }, 1500);
      } else {
        Utils.showError(data.error || "プロジェクトの削除に失敗しました");
      }
    } catch (error) {
      Utils.showError("ネットワークエラーが発生しました");
    }
  },
};

// ナレッジベース関連
const Knowledge = {
  // ナレッジベース削除
  async delete(kbId) {
    if (!Utils.confirm("このナレッジベースを削除しますか？")) {
      return;
    }

    try {
      const { response, data } = await Utils.apiRequest(
        `/api/v1/knowledge/${kbId}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        Utils.showSuccess("ナレッジベースが削除されました");
        setTimeout(() => {
          window.location.reload();
        }, 1500);
      } else {
        Utils.showError(data.error || "ナレッジベースの削除に失敗しました");
      }
    } catch (error) {
      Utils.showError("ネットワークエラーが発生しました");
    }
  },

  // 検索
  async search(kbId, query) {
    try {
      const { response, data } = await Utils.apiRequest(
        `/api/v1/knowledge/${kbId}/search`,
        {
          method: "POST",
          body: JSON.stringify({ query }),
        }
      );

      return response.ok ? data.results : [];
    } catch (error) {
      Utils.showError("検索に失敗しました");
      return [];
    }
  },
};

// 初期化
document.addEventListener("DOMContentLoaded", function () {
  // Bootstrap tooltips有効化
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Bootstrap popovers有効化
  const popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
});

// グローバルに公開
window.Utils = Utils;
window.Auth = Auth;
window.Project = Project;
window.Knowledge = Knowledge;
