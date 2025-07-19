<template>
  <div class="bg-slate-200 rounded-2xl mb-16">
    <div class="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:py-24 lg:px-8">
      <div
        class="flex flex-col lg:flex-row items-center lg:items-start lg:space-x-8"
      >
        <div class="flex-shrink-0">
          <img
            src="@image/profile.png"
            alt="Satoshi Oikawa"
            class="w-32 h-32 rounded-full shadow-lg mx-auto lg:mx-0"
          />
        </div>
        <div class="mt-8 lg:mt-0 text-center lg:text-left">
          <h2 class="text-3xl font-extrabold text-slate-500">開発者</h2>
          <p class="mt-4 text-lg text-slate-400">
            <span class="vidays-font">Vidays</span>は、フリーランスエンジニア
            Satoshi Oikawa とAIによって開発されました。<br />
            独自の機能要望や改善点があれば、ぜひ
            <a
              href="https://github.com/pochaneco/vidays/issues"
              target="_blank"
              class="text-indigo-600 hover:text-indigo-400 underline"
            >
              GitHubのIssueページ
            </a>
            にご提案ください。<br />
            また、導入支援や運用サポートなども可能な範囲で承りますので、お気軽にご相談ください。
          </p>
          <div class="mt-8">
            <a
              href="https://github.com/pochaneco"
              target="_blank"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md bg-slate-600 text-white hover:bg-slate-500"
            >
              View GitHub Profile
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 開発者紹介セクションコンポーネント
</script>
