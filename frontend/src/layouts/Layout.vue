<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- ナビゲーションバー -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <!-- ロゴ -->
            <div class="flex-shrink-0 flex items-center">
              <Link href="/" class="text-xl font-bold text-gray-900">
                AI Knowledge API
              </Link>
            </div>

            <!-- ナビゲーションリンク -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                v-if="$page.props.auth.user"
                href="/projects"
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                プロジェクト
              </Link>
              <Link
                v-if="$page.props.auth.user"
                href="/knowledge"
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                ナレッジ
              </Link>
            </div>
          </div>

          <!-- ユーザーメニュー -->
          <div class="flex items-center">
            <div v-if="$page.props.auth.user" class="ml-3 relative">
              <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-700">
                  {{
                    $page.props.auth.user.display_name ||
                    $page.props.auth.user.username
                  }}
                </span>
                <Link
                  href="/auth/logout"
                  method="post"
                  class="text-sm text-gray-500 hover:text-gray-700"
                >
                  ログアウト
                </Link>
              </div>
            </div>
            <div v-else class="flex items-center space-x-4">
              <Link
                href="/auth/login"
                class="text-sm text-gray-500 hover:text-gray-700"
              >
                ログイン
              </Link>
              <Link
                href="/auth/register"
                class="bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
              >
                登録
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- フラッシュメッセージ -->
    <div
      v-if="flashMessage"
      class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded relative mx-4 mt-4"
      role="alert"
    >
      <span class="block sm:inline">{{ flashMessage }}</span>
    </div>

    <!-- メインコンテンツ -->
    <main class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <slot />
      </div>
    </main>

    <!-- フッター -->
    <footer class="bg-white border-t border-gray-200 mt-auto">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-gray-500">
          © 2024 AI Knowledge API. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { Link } from "@inertiajs/vue3";
import { computed } from "vue";

export default {
  name: "Layout",
  components: {
    Link,
  },
  setup() {
    const flashMessage = computed(() => {
      const flash = this.$page.props.flash;
      return flash?.success || flash?.info || flash?.error;
    });

    return {
      flashMessage,
    };
  },
};
</script>

<style scoped>
/* カスタムスタイルがあればここに追加 */
</style>
