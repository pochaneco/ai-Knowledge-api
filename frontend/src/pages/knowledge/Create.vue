<template>
  <Layout>
    <div class="py-12">
      <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
          <div class="p-6 bg-white border-b border-gray-200">
            <h1 class="text-2xl font-semibold text-gray-900 mb-6">
              {{ knowledge ? "ナレッジを編集" : "新しいナレッジを作成" }}
            </h1>

            <form @submit.prevent="submit" class="space-y-6">
              <!-- タイトル -->
              <div>
                <label
                  for="title"
                  class="block text-sm font-medium text-gray-700"
                >
                  タイトル
                </label>
                <input
                  id="title"
                  v-model="form.title"
                  type="text"
                  required
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="ナレッジのタイトルを入力してください"
                />
                <div v-if="errors.title" class="mt-1 text-sm text-red-600">
                  {{ errors.title }}
                </div>
              </div>

              <!-- カテゴリ -->
              <div>
                <label
                  for="category"
                  class="block text-sm font-medium text-gray-700"
                >
                  カテゴリ
                </label>
                <select
                  id="category"
                  v-model="form.category"
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="">カテゴリを選択してください</option>
                  <option value="Programming">プログラミング</option>
                  <option value="Design">デザイン</option>
                  <option value="Documentation">ドキュメント</option>
                  <option value="Process">プロセス</option>
                  <option value="Other">その他</option>
                </select>
                <div v-if="errors.category" class="mt-1 text-sm text-red-600">
                  {{ errors.category }}
                </div>
              </div>

              <!-- タグ -->
              <div>
                <label
                  for="tags"
                  class="block text-sm font-medium text-gray-700"
                >
                  タグ
                </label>
                <input
                  id="tags"
                  v-model="tagsInput"
                  type="text"
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="タグをカンマ区切りで入力してください（例: Python, Flask, API）"
                />
                <p class="mt-1 text-sm text-gray-500">
                  タグはカンマ（,）で区切って入力してください
                </p>
                <div
                  v-if="form.tags.length > 0"
                  class="mt-2 flex flex-wrap gap-2"
                >
                  <span
                    v-for="tag in form.tags"
                    :key="tag"
                    class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800"
                  >
                    {{ tag }}
                    <button
                      type="button"
                      @click="removeTag(tag)"
                      class="ml-1 text-indigo-600 hover:text-indigo-800"
                    >
                      ×
                    </button>
                  </span>
                </div>
              </div>

              <!-- コンテンツ -->
              <div>
                <label
                  for="content"
                  class="block text-sm font-medium text-gray-700"
                >
                  コンテンツ
                </label>
                <textarea
                  id="content"
                  v-model="form.content"
                  rows="15"
                  required
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="ナレッジの内容を入力してください。マークダウン記法が使用できます。"
                ></textarea>
                <p class="mt-1 text-sm text-gray-500">
                  マークダウン記法（**太字**、*斜体*など）が使用できます
                </p>
                <div v-if="errors.content" class="mt-1 text-sm text-red-600">
                  {{ errors.content }}
                </div>
              </div>

              <!-- プレビュー -->
              <div v-if="form.content" class="border-t pt-6">
                <h3 class="text-lg font-medium text-gray-900 mb-3">
                  プレビュー
                </h3>
                <div class="p-4 border border-gray-200 rounded-md bg-gray-50">
                  <div class="prose max-w-none" v-html="previewContent"></div>
                </div>
              </div>

              <!-- アクションボタン -->
              <div class="flex justify-between items-center pt-6">
                <Link
                  :href="
                    knowledge
                      ? route('knowledge.show', knowledge.id)
                      : route('projects.show', projectId)
                  "
                  class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
                >
                  キャンセル
                </Link>
                <button
                  type="submit"
                  :disabled="form.processing"
                  class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
                >
                  {{
                    form.processing
                      ? "保存中..."
                      : knowledge
                      ? "更新する"
                      : "作成する"
                  }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { reactive, ref, computed, watch } from "vue";
import { Link, router } from "@inertiajs/vue3";
import Layout from "../../layouts/Layout.vue";

const props = defineProps({
  knowledge: {
    type: Object,
    default: null,
  },
  projectId: {
    type: Number,
    required: true,
  },
  errors: {
    type: Object,
    default: () => ({}),
  },
});

const form = reactive({
  title: props.knowledge?.title || "",
  content: props.knowledge?.content || "",
  category: props.knowledge?.category || "",
  tags: props.knowledge?.tags || [],
  project_id: props.projectId,
  processing: false,
});

const tagsInput = ref(form.tags.join(", "));

// タグの処理
watch(tagsInput, (newValue) => {
  form.tags = newValue
    .split(",")
    .map((tag) => tag.trim())
    .filter((tag) => tag.length > 0);
});

const removeTag = (tagToRemove) => {
  form.tags = form.tags.filter((tag) => tag !== tagToRemove);
  tagsInput.value = form.tags.join(", ");
};

// プレビュー
const previewContent = computed(() => {
  return form.content
    .replace(/\n/g, "<br>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/`(.*?)`/g, '<code class="bg-gray-100 px-1 rounded">$1</code>');
});

const submit = () => {
  form.processing = true;

  const url = props.knowledge
    ? route("knowledge.update", props.knowledge.id)
    : route("knowledge.store");

  const method = props.knowledge ? "put" : "post";

  router[method](url, form, {
    onFinish: () => (form.processing = false),
    onSuccess: () => {
      // 成功時の処理は自動的にリダイレクトされる
    },
  });
};
</script>
