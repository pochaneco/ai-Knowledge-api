<template>
  <Layout>
    <div class="py-12">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
          <div class="p-6 bg-white border-b border-gray-200">
            <div class="flex justify-between items-center mb-6">
              <h1 class="text-2xl font-semibold text-gray-900">
                {{ knowledge.title }}
              </h1>
              <div class="flex space-x-2">
                <Link
                  :href="route('knowledge.edit', knowledge.id)"
                  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                  編集
                </Link>
                <button
                  @click="deleteKnowledge"
                  class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                >
                  削除
                </button>
              </div>
            </div>

            <!-- メタ情報 -->
            <div class="flex items-center space-x-4 mb-6 text-sm text-gray-500">
              <span>作成者: {{ knowledge.user.username }}</span>
              <span>•</span>
              <span>作成日: {{ formatDate(knowledge.created_at) }}</span>
              <span>•</span>
              <span>最終更新: {{ formatDate(knowledge.updated_at) }}</span>
              <span v-if="knowledge.category">•</span>
              <span
                v-if="knowledge.category"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                {{ knowledge.category }}
              </span>
            </div>

            <!-- タグ -->
            <div
              v-if="knowledge.tags && knowledge.tags.length > 0"
              class="mb-6"
            >
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in knowledge.tags"
                  :key="tag"
                  class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-gray-100 text-gray-800"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- コンテンツ -->
            <div class="prose max-w-none">
              <div v-html="formattedContent"></div>
            </div>

            <!-- 関連ナレッジ -->
            <div v-if="relatedKnowledge.length > 0" class="mt-8">
              <h2 class="text-xl font-semibold text-gray-900 mb-4">
                関連するナレッジ
              </h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Link
                  v-for="related in relatedKnowledge"
                  :key="related.id"
                  :href="route('knowledge.show', related.id)"
                  class="block p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
                >
                  <h3 class="font-medium text-indigo-600 hover:text-indigo-800">
                    {{ related.title }}
                  </h3>
                  <p class="text-gray-600 text-sm mt-1">
                    {{ related.content.substring(0, 100) }}...
                  </p>
                  <div class="flex items-center mt-2 text-xs text-gray-500">
                    <span>{{ related.user.username }}</span>
                    <span class="mx-1">•</span>
                    <span>{{ formatDate(related.created_at) }}</span>
                  </div>
                </Link>
              </div>
            </div>

            <!-- AI検索ボックス -->
            <div class="mt-8 p-4 bg-gray-50 rounded-lg">
              <h3 class="text-lg font-medium text-gray-900 mb-3">
                AI検索で関連情報を探す
              </h3>
              <div class="flex space-x-2">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="自然言語で検索してください..."
                  class="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  @keyup.enter="performAISearch"
                />
                <button
                  @click="performAISearch"
                  :disabled="!searchQuery.trim() || searching"
                  class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
                >
                  {{ searching ? "検索中..." : "検索" }}
                </button>
              </div>

              <!-- 検索結果 -->
              <div v-if="searchResults.length > 0" class="mt-4">
                <h4 class="font-medium text-gray-900 mb-2">検索結果</h4>
                <div class="space-y-2">
                  <Link
                    v-for="result in searchResults"
                    :key="result.id"
                    :href="route('knowledge.show', result.id)"
                    class="block p-3 border border-gray-200 rounded hover:bg-gray-50"
                  >
                    <h5 class="font-medium text-indigo-600">
                      {{ result.title }}
                    </h5>
                    <p class="text-sm text-gray-600">{{ result.snippet }}</p>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref } from "vue";
import { Link, router } from "@inertiajs/vue3";
import Layout from "../../layouts/Layout.vue";

const props = defineProps({
  knowledge: Object,
  relatedKnowledge: {
    type: Array,
    default: () => [],
  },
});

const searchQuery = ref("");
const searchResults = ref([]);
const searching = ref(false);

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("ja-JP");
};

const formattedContent = computed(() => {
  // 簡単なマークダウン風のフォーマッティング
  return props.knowledge.content
    .replace(/\n/g, "<br>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>");
});

const deleteKnowledge = () => {
  if (confirm("本当にこのナレッジを削除しますか？この操作は取り消せません。")) {
    router.delete(route("knowledge.destroy", props.knowledge.id));
  }
};

const performAISearch = async () => {
  if (!searchQuery.value.trim()) return;

  searching.value = true;
  try {
    const response = await fetch("/api/v1/knowledge/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": document
          .querySelector('meta[name="csrf-token"]')
          .getAttribute("content"),
      },
      body: JSON.stringify({
        query: searchQuery.value,
        project_id: props.knowledge.project_id,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      searchResults.value = data.results || [];
    }
  } catch (error) {
    console.error("検索エラー:", error);
  } finally {
    searching.value = false;
  }
};
</script>
