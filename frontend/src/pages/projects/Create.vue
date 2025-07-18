<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h1 class="text-xl font-semibold text-gray-900 mb-6">
            新しいプロジェクトを作成
          </h1>

          <form @submit.prevent="submit" class="space-y-6">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">
                プロジェクト名
              </label>
              <div class="mt-1">
                <input
                  id="name"
                  v-model="form.name"
                  name="name"
                  type="text"
                  required
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="プロジェクト名を入力"
                />
              </div>
              <div v-if="form.errors.name" class="mt-2 text-sm text-red-600">
                {{ form.errors.name }}
              </div>
            </div>

            <div>
              <label
                for="description"
                class="block text-sm font-medium text-gray-700"
              >
                説明
              </label>
              <div class="mt-1">
                <textarea
                  id="description"
                  v-model="form.description"
                  name="description"
                  rows="4"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="プロジェクトの説明を入力"
                ></textarea>
              </div>
              <div
                v-if="form.errors.description"
                class="mt-2 text-sm text-red-600"
              >
                {{ form.errors.description }}
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">
                プライバシー設定
              </label>
              <div class="mt-2 space-y-2">
                <div class="flex items-center">
                  <input
                    id="private"
                    v-model="form.is_private"
                    name="is_private"
                    type="radio"
                    :value="true"
                    class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                  />
                  <label
                    for="private"
                    class="ml-3 block text-sm font-medium text-gray-700"
                  >
                    プライベート - 招待されたメンバーのみアクセス可能
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="public"
                    v-model="form.is_private"
                    name="is_private"
                    type="radio"
                    :value="false"
                    class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                  />
                  <label
                    for="public"
                    class="ml-3 block text-sm font-medium text-gray-700"
                  >
                    パブリック - 誰でもアクセス可能
                  </label>
                </div>
              </div>
            </div>

            <div class="flex justify-end space-x-3">
              <Link
                :href="route('project.index')"
                class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                キャンセル
              </Link>
              <button
                type="submit"
                :disabled="form.processing"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {{ form.processing ? "作成中..." : "プロジェクトを作成" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Head, Link, useForm } from "@inertiajs/vue3";

export default {
  components: {
    Head,
    Link,
  },
  setup() {
    const form = useForm({
      name: "",
      description: "",
      is_private: true,
    });

    const submit = () => {
      form.post(route("project.store"));
    };

    return {
      form,
      submit,
    };
  },
};
</script>
