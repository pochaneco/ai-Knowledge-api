<template>
  <div class="my-32 rounded-xl bg-gradient-to-r from-indigo-400 to-indigo-600">
    <div
      class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between"
    >
      <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
        <span class="block">今すぐ始めよう</span>
        <span class="block text-indigo-200"
          >AIエージェントと知識を最大限に活用しませんか？</span
        >
      </h2>
      <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
        <div class="inline-flex rounded-md shadow">
          <Link
            v-if="!$page.props.auth.user"
            href="/auth/register"
            class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md bg-orange-600 text-white hover:bg-orange-700"
          >
            無料で始める
          </Link>
          <Link
            v-else
            href="/projects"
            class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md bg-orange-600 text-white hover:bg-orange-700"
          >
            プロジェクトを見る
          </Link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Link } from "@inertiajs/vue3";
</script>
