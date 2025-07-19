<template>
  <div class="bg-indigo-800">
    <div class="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:py-24 lg:px-8">
      <div class="max-w-3xl mx-auto text-center">
        <h2 class="text-3xl font-extrabold text-white">
          このようなことでお困りではありませんか？
        </h2>
        <p class="mt-4 text-lg text-indigo-200">
          <span class="vidays-font">Vidays</span
          >は、あなたの抱える課題を解決するためのツールです。
        </p>
      </div>
      <div class="mt-12 grid gap-8 lg:grid-cols-3">
        <div class="bg-indigo-700 p-6 rounded-lg shadow-lg">
          <p class="text-lg text-white">"大きなタスクが途中で混乱する"</p>
          <p class="mt-4 text-sm text-indigo-200">
            <span class="vidays-font">Vidays</span
            >はタスクを小さく分けてAIの処理能力を最大限に活用し、効率的に進める方法を提案します。複雑な作業もスムーズに進められるようサポートします。
          </p>
        </div>
        <div class="bg-indigo-700 p-6 rounded-lg shadow-lg">
          <p class="text-lg text-white">"専門的な知識が必要な作業が難しい"</p>
          <p class="mt-4 text-sm text-indigo-200">
            <span class="vidays-font">Vidays</span
            >は専門分野に特化したAIと知識ベースを活用し、あなたの作業を強力にサポートします。
          </p>
        </div>
        <div class="bg-indigo-700 p-6 rounded-lg shadow-lg">
          <p class="text-lg text-white">"AIが間違った情報を出して困る"</p>
          <p class="mt-4 text-sm text-indigo-200">
            <span class="vidays-font">Vidays</span
            >は信頼できる情報源を活用し、正確な回答を提供します。間違いを防ぐ仕組みも整っています。
          </p>
        </div>
        <div class="bg-indigo-700 p-6 rounded-lg shadow-lg">
          <p class="text-lg text-white">"コストを抑えながら成果を出したい"</p>
          <p class="mt-4 text-sm text-indigo-200">
            <span class="vidays-font">Vidays</span
            >はタスクに最適なAIを選び、コストを抑えつつ高い成果を実現します。
          </p>
        </div>
        <div class="bg-indigo-700 p-6 rounded-lg shadow-lg">
          <p class="text-lg text-white">"もっと自然で複雑な会話がしたい"</p>
          <p class="mt-4 text-sm text-indigo-200">
            <span class="vidays-font">Vidays</span
            >はあなたの意図を深く理解し、自然で的確な対話を実現します。複雑な質問にも対応可能です。
          </p>
        </div>
        <div class="bg-indigo-700 p-6 rounded-lg shadow-lg">
          <p class="text-lg text-white">"自社システムにAIを統合したい"</p>
          <p class="mt-4 text-sm text-indigo-200">
            <span class="vidays-font">Vidays</span
            >は柔軟なAPIを提供し、既存のシステムに簡単に統合できます。カスタマイズも可能で、あなたのビジネスに最適なソリューションを提供します。
          </p>
        </div>
      </div>
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
</template>

<script setup>
import { Link } from "@inertiajs/vue3";
</script>
