<template>
  <component
    :is="iconComponent"
    :class="[sizeClass, colorClass, customClass]"
    v-bind="$attrs"
  />
</template>

<script setup>
import { computed } from "vue";
import {
  BoltIcon,
  ServerIcon,
  UsersIcon,
  CogIcon,
  DocumentTextIcon,
  SparklesIcon,
  ArchiveBoxIcon,
  PuzzlePieceIcon,
  ShareIcon,
  CommandLineIcon,
} from "@heroicons/vue/24/outline";

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  size: {
    type: String,
    default: "md",
    validator: (value) => ["xs", "sm", "md", "lg", "xl"].includes(value),
  },
  color: {
    type: String,
    default: "current",
  },
  class: {
    type: String,
    default: "",
  },
});

// アイコンマッピング
const iconMap = {
  bolt: BoltIcon,
  lightning: BoltIcon,
  server: ServerIcon,
  database: ServerIcon,
  archive: ArchiveBoxIcon,
  knowledge: ArchiveBoxIcon,
  users: UsersIcon,
  team: UsersIcon,
  share: ShareIcon,
  collaboration: ShareIcon,
  cog: CogIcon,
  settings: CogIcon,
  puzzle: PuzzlePieceIcon,
  model: PuzzlePieceIcon,
  command: CommandLineIcon,
  task: CommandLineIcon,
  document: DocumentTextIcon,
  file: DocumentTextIcon,
  sparkles: SparklesIcon,
  ai: SparklesIcon,
};

// アイコンコンポーネントを取得
const iconComponent = computed(() => {
  return iconMap[props.name] || BoltIcon;
});

// サイズクラス
const sizeClass = computed(() => {
  const sizes = {
    xs: "h-3 w-3",
    sm: "h-4 w-4",
    md: "h-6 w-6",
    lg: "h-8 w-8",
    xl: "h-12 w-12",
  };
  return sizes[props.size] || sizes.md;
});

// カラークラス
const colorClass = computed(() => {
  if (props.color === "current") return "text-current";
  if (props.color === "white") return "text-white";
  return `text-${props.color}`;
});

// カスタムクラス
const customClass = computed(() => props.class);
</script>
