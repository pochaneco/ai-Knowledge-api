<template>
  <div class="bg-indigo-900">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8">
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-white">
          <span class="vidays-font">Vidays</span>を今すぐ始めましょう
        </h2>
        <p class="mt-4 text-lg text-indigo-200">
          AIを効率的に活用し、日々の活動をよりクリエイティブに
        </p>
        <div class="mt-8 flex justify-center">
          <div class="inline-flex rounded-md shadow">
            <Link
              href="/auth/register"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md bg-orange-600 text-white hover:bg-orange-700"
            >
              無料で始める
            </Link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Link } from "@inertiajs/vue3";
</script>
