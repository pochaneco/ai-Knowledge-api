<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-indigo-800 to-orange-900 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-white">
          メールアドレスの認証
        </h2>
        <p class="mt-2 text-center text-sm text-indigo-200">
          メールアドレスの認証を行っています...
        </p>
      </div>

      <div v-if="verificationStatus === 'processing'" class="text-center">
        <div
          class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-400 mx-auto"
        ></div>
        <p class="mt-4 text-sm text-indigo-200">認証中...</p>
      </div>

      <div v-else-if="verificationStatus === 'success'" class="text-center">
        <div class="text-green-400 text-6xl mb-4">✓</div>
        <p class="text-lg font-medium text-white">
          メールアドレスが認証されました
        </p>
        <p class="mt-2 text-sm text-indigo-200">
          ログインページに移動します...
        </p>
      </div>

      <div v-else-if="verificationStatus === 'error'" class="text-center">
        <div class="text-red-400 text-6xl mb-4">✗</div>
        <p class="text-lg font-medium text-white">認証に失敗しました</p>
        <p class="mt-2 text-sm text-indigo-200">
          リンクが無効か期限切れの可能性があります
        </p>
        <div class="mt-4">
          <Link
            :href="route('auth.login')"
            class="font-medium text-orange-400 hover:text-orange-300"
          >
            ログインページに戻る
          </Link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Head, Link, router } from "@inertiajs/vue3";
import { ref, onMounted } from "vue";

export default {
  components: {
    Head,
    Link,
  },
  props: {
    token: String,
  },
  setup(props) {
    const verificationStatus = ref("processing");

    const verifyEmail = async () => {
      try {
        await router.post(
          route("auth.verify-email", { token: props.token }),
          {},
          {
            onSuccess: () => {
              verificationStatus.value = "success";
              setTimeout(() => {
                router.visit(route("auth.login"));
              }, 2000);
            },
            onError: () => {
              verificationStatus.value = "error";
            },
          }
        );
      } catch (error) {
        verificationStatus.value = "error";
      }
    };

    onMounted(() => {
      verifyEmail();
    });

    return {
      verificationStatus,
    };
  },
};
</script>
