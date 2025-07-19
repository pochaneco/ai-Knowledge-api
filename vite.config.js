import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// 環境に応じてHMRポートを設定
// .envで指定されたポートをコンテナ内でも使用
console.log("VITE_PORT:", process.env.VITE_PORT);
const vitePort = process.env.VITE_PORT ? parseInt(process.env.VITE_PORT) : 5173;

export default defineConfig({
  plugins: [
    vue({
      template: {
        transformAssetUrls: {
          base: null,
          includeAbsolute: false,
        },
      },
    }),
  ],
  resolve: {
    alias: {
      "@": resolve(__dirname, "frontend/src"),
      "@image": resolve(__dirname, "frontend/src/assets"),
    },
  },
  build: {
    outDir: "../app/static/dist",
    rollupOptions: {
      input: {
        app: resolve(__dirname, "frontend/src/app.js"),
      },
    },
    manifest: true,
  },
  server: {
    host: "0.0.0.0",
    port: vitePort,
    hmr: {
      host: "localhost",
      port: vitePort,
    },
    origin: "http://localhost:" + vitePort,
  },
  root: "frontend",
});
