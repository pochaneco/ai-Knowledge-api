<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="sm:flex sm:items-center">
            <div class="sm:flex-auto">
              <h1 class="text-xl font-semibold text-gray-900">プロジェクト</h1>
              <p class="mt-2 text-sm text-gray-700">プロジェクトの一覧と管理</p>
            </div>
            <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
              <Link
                :href="route('project.create')"
                class="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                新しいプロジェクト
              </Link>
            </div>
          </div>

          <div class="mt-8 flow-root">
            <div class="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
              <div
                class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8"
              >
                <div
                  class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg"
                >
                  <table class="min-w-full divide-y divide-gray-300">
                    <thead class="bg-gray-50">
                      <tr>
                        <th
                          scope="col"
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide"
                        >
                          プロジェクト名
                        </th>
                        <th
                          scope="col"
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide"
                        >
                          説明
                        </th>
                        <th
                          scope="col"
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide"
                        >
                          メンバー数
                        </th>
                        <th
                          scope="col"
                          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide"
                        >
                          作成日
                        </th>
                        <th scope="col" class="relative px-6 py-3">
                          <span class="sr-only">操作</span>
                        </th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="project in projects" :key="project.id">
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                        >
                          <Link
                            :href="
                              route('project.detail', {
                                project_id: project.id,
                              })
                            "
                            class="text-indigo-600 hover:text-indigo-900"
                          >
                            {{ project.name }}
                          </Link>
                        </td>
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                        >
                          {{ project.description }}
                        </td>
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                        >
                          {{ project.member_count }}
                        </td>
                        <td
                          class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                        >
                          {{ formatDate(project.created_at) }}
                        </td>
                        <td
                          class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                        >
                          <Link
                            :href="
                              route('project.edit', { project_id: project.id })
                            "
                            class="text-indigo-600 hover:text-indigo-900 mr-4"
                          >
                            編集
                          </Link>
                          <Link
                            :href="
                              route('project.members', {
                                project_id: project.id,
                              })
                            "
                            class="text-indigo-600 hover:text-indigo-900"
                          >
                            メンバー
                          </Link>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Head, Link } from "@inertiajs/vue3";

export default {
  components: {
    Head,
    Link,
  },
  props: {
    projects: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString("ja-JP");
    };

    return {
      formatDate,
    };
  },
};
</script>
