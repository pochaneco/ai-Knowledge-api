<template>
  <Layout>
    <div class="py-12">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
          <div class="p-6 bg-white border-b border-gray-200">
            <div class="flex justify-between items-center mb-6">
              <h1 class="text-2xl font-semibold text-gray-900">
                {{ project.name }}
              </h1>
              <div class="flex space-x-2">
                <Link
                  :href="route('projects.edit', project.id)"
                  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                  編集
                </Link>
                <button
                  @click="deleteProject"
                  class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                >
                  削除
                </button>
              </div>
            </div>

            <div class="mb-6">
              <p class="text-gray-600">{{ project.description }}</p>
            </div>

            <!-- プロジェクト統計 -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold text-blue-900">メンバー数</h3>
                <p class="text-2xl font-bold text-blue-600">
                  {{ project.members_count }}
                </p>
              </div>
              <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold text-green-900">ナレッジ数</h3>
                <p class="text-2xl font-bold text-green-600">
                  {{ project.knowledge_count }}
                </p>
              </div>
              <div class="bg-purple-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold text-purple-900">最終更新</h3>
                <p class="text-sm text-purple-600">
                  {{ formatDate(project.updated_at) }}
                </p>
              </div>
            </div>

            <!-- メンバー一覧 -->
            <div class="mb-8">
              <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold text-gray-900">メンバー</h2>
                <Link
                  :href="route('projects.members.invite', project.id)"
                  class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                  メンバーを招待
                </Link>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div
                  v-for="member in project.members"
                  :key="member.id"
                  class="bg-gray-50 p-4 rounded-lg"
                >
                  <div class="flex items-center space-x-3">
                    <div class="flex-shrink-0">
                      <div
                        class="h-8 w-8 bg-gray-300 rounded-full flex items-center justify-center"
                      >
                        <span class="text-sm font-medium text-gray-700">
                          {{ member.username.charAt(0).toUpperCase() }}
                        </span>
                      </div>
                    </div>
                    <div class="flex-1">
                      <p class="text-sm font-medium text-gray-900">
                        {{ member.username }}
                      </p>
                      <p class="text-sm text-gray-500">
                        {{ member.pivot.role }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- ナレッジベース一覧 -->
            <div>
              <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold text-gray-900">
                  ナレッジベース
                </h2>
                <Link
                  :href="route('knowledge.create', { project: project.id })"
                  class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"
                >
                  新しいナレッジ
                </Link>
              </div>
              <div class="space-y-4">
                <div
                  v-for="knowledge in project.knowledge_bases"
                  :key="knowledge.id"
                  class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <Link
                        :href="route('knowledge.show', knowledge.id)"
                        class="text-lg font-medium text-indigo-600 hover:text-indigo-800"
                      >
                        {{ knowledge.title }}
                      </Link>
                      <p class="text-gray-600 mt-1">
                        {{ knowledge.content.substring(0, 150) }}...
                      </p>
                      <div class="flex items-center mt-2 text-sm text-gray-500">
                        <span>作成者: {{ knowledge.user.username }}</span>
                        <span class="mx-2">•</span>
                        <span>{{ formatDate(knowledge.created_at) }}</span>
                      </div>
                    </div>
                    <div class="ml-4">
                      <span
                        v-if="knowledge.category"
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                      >
                        {{ knowledge.category }}
                      </span>
                    </div>
                  </div>
                </div>
                <div
                  v-if="project.knowledge_bases.length === 0"
                  class="text-center py-8"
                >
                  <p class="text-gray-500">まだナレッジベースがありません。</p>
                  <Link
                    :href="route('knowledge.create', { project: project.id })"
                    class="text-indigo-600 hover:text-indigo-800 font-medium"
                  >
                    最初のナレッジを作成しましょう
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
import { Link, router } from "@inertiajs/vue3";
import Layout from "../../layouts/Layout.vue";

const props = defineProps({
  project: Object,
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("ja-JP");
};

const deleteProject = () => {
  if (
    confirm("本当にこのプロジェクトを削除しますか？この操作は取り消せません。")
  ) {
    router.delete(route("projects.destroy", props.project.id));
  }
};
</script>
