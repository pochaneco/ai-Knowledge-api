<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-indigo-800 to-orange-900 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-white">
          パスワードをリセット
        </h2>
        <p class="mt-2 text-center text-sm text-indigo-200">
          メールアドレスを入力してください。リセット用のリンクをお送りします。
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="submit">
        <div>
          <label for="email" class="sr-only">メールアドレス</label>
          <input
            id="email"
            v-model="form.email"
            name="email"
            type="email"
            required
            class="appearance-none relative block w-full px-3 py-2 border border-indigo-600 placeholder-indigo-300 text-white bg-indigo-700 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm"
            placeholder="メールアドレス"
          />
        </div>

        <div>
          <button
            type="submit"
            :disabled="form.processing"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50"
          >
            {{ form.processing ? "送信中..." : "リセットリンクを送信" }}
          </button>
        </div>

        <div class="text-center">
          <Link
            :href="route('auth.login')"
            class="font-medium text-orange-400 hover:text-orange-300"
          >
            ログインページに戻る
          </Link>
        </div>
      </form>
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
      email: "",
    });

    const submit = () => {
      form.post(route("auth.forgot-password"));
    };

    return {
      form,
      submit,
    };
  },
};
</script>
