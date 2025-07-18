<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="sm:flex sm:items-center">
            <div class="sm:flex-auto">
              <h1 class="text-xl font-semibold text-gray-900">
                ナレッジベース
              </h1>
              <p class="mt-2 text-sm text-gray-700">知識とドキュメントの管理</p>
            </div>
            <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
              <Link
                :href="route('knowledge.create')"
                class="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                新しいナレッジ
              </Link>
            </div>
          </div>

          <!-- 検索フォーム -->
          <div class="mt-6">
            <div class="flex space-x-4">
              <div class="flex-1">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="ナレッジを検索..."
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  @keyup.enter="search"
                />
              </div>
              <button
                @click="search"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                検索
              </button>
            </div>
          </div>

          <!-- ナレッジリスト -->
          <div class="mt-8">
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              <div
                v-for="knowledge in knowledgeList"
                :key="knowledge.id"
                class="bg-white overflow-hidden shadow rounded-lg border border-gray-200 hover:shadow-md transition-shadow duration-200"
              >
                <div class="p-6">
                  <div class="flex items-center">
                    <div class="flex-shrink-0">
                      <div
                        class="h-10 w-10 bg-indigo-500 rounded-lg flex items-center justify-center"
                      >
                        <svg
                          class="h-6 w-6 text-white"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                          />
                        </svg>
                      </div>
                    </div>
                    <div class="ml-4 flex-1">
                      <Link
                        :href="
                          route('knowledge.detail', { kb_id: knowledge.id })
                        "
                        class="text-sm font-medium text-gray-900 hover:text-indigo-600"
                      >
                        {{ knowledge.title }}
                      </Link>
                      <p class="text-sm text-gray-500">
                        {{ knowledge.category }}
                      </p>
                    </div>
                  </div>
                  <div class="mt-4">
                    <p class="text-sm text-gray-600 line-clamp-3">
                      {{ knowledge.content }}
                    </p>
                  </div>
                  <div class="mt-4 flex items-center justify-between">
                    <div class="flex flex-wrap gap-1">
                      <span
                        v-for="tag in knowledge.tags"
                        :key="tag"
                        class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-indigo-100 text-indigo-800"
                      >
                        {{ tag }}
                      </span>
                    </div>
                    <div class="flex space-x-2">
                      <Link
                        :href="route('knowledge.edit', { kb_id: knowledge.id })"
                        class="text-indigo-600 hover:text-indigo-900 text-sm"
                      >
                        編集
                      </Link>
                    </div>
                  </div>
                  <div class="mt-2 text-xs text-gray-400">
                    {{ formatDate(knowledge.created_at) }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 空の状態 -->
          <div v-if="knowledgeList.length === 0" class="text-center py-12">
            <svg
              class="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">
              ナレッジがありません
            </h3>
            <p class="mt-1 text-sm text-gray-500">
              新しいナレッジを作成してみましょう。
            </p>
            <div class="mt-6">
              <Link
                :href="route('knowledge.create')"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                新しいナレッジを作成
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Head, Link, router } from "@inertiajs/vue3";
import { ref } from "vue";

export default {
  components: {
    Head,
    Link,
  },
  props: {
    knowledgeList: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const searchQuery = ref("");

    const search = () => {
      if (searchQuery.value.trim()) {
        router.get(
          route("knowledge.search"),
          { q: searchQuery.value },
          {
            preserveState: true,
            preserveScroll: true,
          }
        );
      }
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString("ja-JP");
    };

    return {
      searchQuery,
      search,
      formatDate,
    };
  },
};
</script>
