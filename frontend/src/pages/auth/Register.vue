<template>
  <div
    class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div
      class="max-w-md w-full space-y-8 bg-indigo-800 p-8 rounded-lg shadow-xl"
    >
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-white">
          アカウントを作成
        </h2>
        <p class="mt-2 text-center text-sm text-indigo-200">
          または
          <Link
            :href="route('auth.login')"
            class="font-medium text-orange-300 hover:text-orange-200"
          >
            既存のアカウントでログイン
          </Link>
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="submit">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">ユーザー名</label>
            <input
              id="username"
              v-model="form.username"
              name="username"
              type="text"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-indigo-600 placeholder-indigo-300 text-white bg-indigo-700 rounded-t-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm"
              placeholder="ユーザー名"
            />
          </div>
          <div>
            <label for="email" class="sr-only">メールアドレス</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-indigo-600 placeholder-indigo-300 text-white bg-indigo-700 focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm"
              placeholder="メールアドレス"
            />
          </div>
          <div>
            <label for="password" class="sr-only">パスワード</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-indigo-600 placeholder-indigo-300 text-white bg-indigo-700 focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm"
              placeholder="パスワード"
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
            {{ form.processing ? "登録中..." : "アカウント作成" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { Head, Link, useForm } from "@inertiajs/vue3";
import { route } from "../../utils/routes";

export default {
  components: {
    Head,
    Link,
  },
  setup() {
    const form = useForm({
      username: "",
      email: "",
      password: "",
      password_confirmation: "",
    });

    const submit = () => {
      form.post("/api/v1/auth/register", {
        onFinish: () => form.reset("password", "password_confirmation"),
      });
    };

    return {
      form,
      submit,
      route,
    };
  },
};
</script>
