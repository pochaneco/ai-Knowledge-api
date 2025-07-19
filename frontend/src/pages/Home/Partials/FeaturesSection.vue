<template>
  <div class="bg-indigo-900">
    <div class="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:py-24 lg:px-8">
      <div class="max-w-3xl mx-auto text-center">
        <h2 class="text-3xl font-extrabold text-white">主な機能</h2>
        <p class="mt-4 text-lg text-indigo-200">
          チームの力を最大化するための革新的なツールセット
        </p>
      </div>
      <dl
        class="mt-12 space-y-10 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-x-6 sm:gap-y-12 lg:grid-cols-3 lg:gap-x-8"
      >
        <div class="relative">
          <dt>
            <div
              class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white"
            >
              <Icon name="bolt" size="md" color="white" />
            </div>
            <p class="ml-16 text-lg leading-6 font-medium text-white">
              AIエージェント
            </p>
          </dt>
          <dd class="mt-2 ml-16 text-base text-indigo-200">
            AIで知識の探索と整理を次のレベルへ
          </dd>
        </div>

        <div class="relative">
          <dt>
            <div
              class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white"
            >
              <Icon name="archive" size="md" color="white" />
            </div>
            <p class="ml-16 text-lg leading-6 font-medium text-white">
              知識データベース
            </p>
          </dt>
          <dd class="mt-2 ml-16 text-base text-indigo-200">
            知識をスマートに管理
          </dd>
        </div>

        <div class="relative">
          <dt>
            <div
              class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white"
            >
              <Icon name="users" size="md" color="white" />
            </div>
            <p class="ml-16 text-lg leading-6 font-medium text-white">
              チーム共有
            </p>
          </dt>
          <dd class="mt-2 ml-16 text-base text-indigo-200">
            シームレスなコラボレーション
          </dd>
        </div>

        <div class="relative">
          <dt>
            <div
              class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white"
            >
              <Icon name="puzzle" size="md" color="white" />
            </div>
            <p class="ml-16 text-lg leading-6 font-medium text-white">
              モデル選択
            </p>
          </dt>
          <dd class="mt-2 ml-16 text-base text-indigo-200">
            タスクに最適なAIの選択
          </dd>
        </div>

        <div class="relative">
          <dt>
            <div
              class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white"
            >
              <Icon name="command" size="md" color="white" />
            </div>
            <p class="ml-16 text-lg leading-6 font-medium text-white">
              タスク分割・管理
            </p>
          </dt>
          <dd class="mt-2 ml-16 text-base text-indigo-200">
            複雑なタスクを分割し並列処理
          </dd>
        </div>

        <div class="relative">
          <dt>
            <div
              class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white"
            >
              <svg
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
            </div>
            <p class="ml-16 text-lg leading-6 font-medium text-white">
              多様なファイル読込 (今後)
            </p>
          </dt>
          <dd class="mt-2 ml-16 text-base text-indigo-200">
            さまざまな形式のファイルを処理する機能の実装予定
          </dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<script setup>
import Icon from "../../../components/Icon.vue";
</script>
