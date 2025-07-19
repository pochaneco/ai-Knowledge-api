<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-indigo-800 to-orange-900 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-white">
          新しいパスワードを設定
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="submit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="password" class="sr-only">新しいパスワード</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-indigo-600 placeholder-indigo-300 text-white bg-indigo-700 rounded-t-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm"
              placeholder="新しいパスワード"
            />
          </div>
          <div>
            <label for="password_confirmation" class="sr-only"
              >パスワード確認</label
            >
            <input
              id="password_confirmation"
              v-model="form.password_confirmation"
              name="password_confirmation"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-indigo-600 placeholder-indigo-300 text-white bg-indigo-700 rounded-b-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm"
              placeholder="パスワード確認"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="form.processing"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50"
          >
            {{ form.processing ? "更新中..." : "パスワードを更新" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { Head, useForm } from "@inertiajs/vue3";

export default {
  components: {
    Head,
  },
  props: {
    token: String,
  },
  setup(props) {
    const form = useForm({
      token: props.token,
      password: "",
      password_confirmation: "",
    });

    const submit = () => {
      form.post(route("auth.reset-password", { token: props.token }), {
        onFinish: () => form.reset("password", "password_confirmation"),
      });
    };

    return {
      form,
      submit,
    };
  },
};
</script>
