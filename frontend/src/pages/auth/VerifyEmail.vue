<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          メールアドレスの認証
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          メールアドレスの認証を行っています...
        </p>
      </div>

      <div v-if="verificationStatus === 'processing'" class="text-center">
        <div
          class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"
        ></div>
        <p class="mt-4 text-sm text-gray-600">認証中...</p>
      </div>

      <div v-else-if="verificationStatus === 'success'" class="text-center">
        <div class="text-green-600 text-6xl mb-4">✓</div>
        <p class="text-lg font-medium text-gray-900">
          メールアドレスが認証されました
        </p>
        <p class="mt-2 text-sm text-gray-600">ログインページに移動します...</p>
      </div>

      <div v-else-if="verificationStatus === 'error'" class="text-center">
        <div class="text-red-600 text-6xl mb-4">✗</div>
        <p class="text-lg font-medium text-gray-900">認証に失敗しました</p>
        <p class="mt-2 text-sm text-gray-600">
          リンクが無効か期限切れの可能性があります
        </p>
        <div class="mt-4">
          <Link
            :href="route('auth.login')"
            class="font-medium text-indigo-600 hover:text-indigo-500"
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
