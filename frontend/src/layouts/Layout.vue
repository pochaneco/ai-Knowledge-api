<template>
  <div id="app" class="min-h-screen bg-indigo-800">
    <!-- ナビゲーションバー -->
    <nav class="bg-indigo-900 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <!-- ロゴ -->
            <div class="flex-shrink-0 flex items-center">
              <img src="@image/icon.png" alt="Vidays Logo" class="h-12" />
              <Link href="/" class="text-xl vidays-font font-bold text-white">
                Vidays
              </Link>
            </div>

            <!-- ナビゲーションリンク -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                v-if="page.props.auth?.user"
                href="/projects"
                class="border-transparent text-white hover:border-indigo-300 hover:text-indigo-100 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                プロジェクト
              </Link>
              <Link
                v-if="page.props.auth?.user"
                href="/knowledge"
                class="border-transparent text-white hover:border-indigo-300 hover:text-indigo-100 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                ナレッジ
              </Link>
            </div>
          </div>

          <!-- ユーザーメニュー -->
          <div class="flex items-center">
            <div v-if="page.props.auth?.user" class="ml-3 relative">
              <div class="flex items-center space-x-4">
                <span class="text-sm text-white">
                  {{
                    page.props.auth.user.display_name ||
                    page.props.auth.user.username
                  }}
                </span>
                <Link
                  href="/auth/logout"
                  method="post"
                  class="text-sm text-indigo-200 hover:text-white"
                >
                  ログアウト
                </Link>
              </div>
            </div>
            <div v-else class="flex items-center space-x-4">
              <Link
                href="/auth/login"
                class="text-sm text-indigo-200 hover:text-white"
              >
                ログイン
              </Link>
              <Link
                href="/auth/register"
                class="bg-orange-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-orange-500"
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
    <main class="mb-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <slot />
      </div>
    </main>

    <!-- フッター -->
    <footer class="bg-indigo-900 text-center py-2 mt-auto">
      <p class="text-sm text-indigo-300">
        © 2025 Vidays. Released under the
        <a
          href="https://opensource.org/licenses/MIT"
          target="_blank"
          class="text-indigo-200 hover:text-white underline"
        >
          MIT License </a
        >.
      </p>
      <p class="mt-2 text-xs text-indigo-400">
        このソフトウェアはMITライセンスの下で配布されています。詳細については上記のリンクをご確認ください。
      </p>
    </footer>
  </div>
</template>

<script>
import { Link, usePage } from "@inertiajs/vue3";
import { computed } from "vue";

export default {
  name: "Layout",
  components: {
    Link,
  },
  setup() {
    const page = usePage();

    const flashMessage = computed(() => {
      const flash = page.props?.flash;
      return flash?.success || flash?.info || flash?.error;
    });

    return {
      page,
      flashMessage,
    };
  },
};
</script>

<style scoped>
/* カスタムスタイルがあればここに追加 */
</style>
