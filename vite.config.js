import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "frontend/src"),
    },
  },
  build: {
    outDir: "app/static/dist",
    rollupOptions: {
      input: {
        app: resolve(__dirname, "frontend/src/app.js"),
      },
    },
    manifest: true,
  },
  server: {
    host: "0.0.0.0",
    port: process.env.VITE_PORT ? parseInt(process.env.VITE_PORT) : 5173,
    hmr: {
      host: "localhost",
      port: process.env.VITE_PORT ? parseInt(process.env.VITE_PORT) : 5173,
    },
  },
  root: "frontend",
});
