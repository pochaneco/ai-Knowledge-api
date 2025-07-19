import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";
import { resolvePageComponent } from "./utils/resolvePageComponent";
import Layout from "./layouts/Layout.vue";
import { route } from "./utils/routes";
import "./app.css";

// 初期ページデータを取得
const el = document.getElementById("app");
const pageData = el.dataset.page;

console.log("Raw page data:", pageData);

let initialPage;
try {
  initialPage = JSON.parse(pageData);
  console.log("Parsed page data:", initialPage);
} catch (error) {
  console.error("JSON parse error:", error);
  console.error("Raw data causing error:", pageData);
  // フォールバック用のデフォルトページデータ
  initialPage = {
    component: "Welcome",
    props: {},
    url: window.location.href,
    version: "1.0.0",
  };
}

createInertiaApp({
  id: "app",
  resolve: async (name) => {
    console.log("Resolving page:", name);
    try {
      const page = await resolvePageComponent(
        name,
        import.meta.glob("./pages/**/*.vue")
      );
      page.default.layout = page.default.layout || Layout;
      console.log("Page resolved:", page);
      return page;
    } catch (error) {
      console.error("Page resolution error:", error);
      // フォールバック: 存在しないページの場合はWelcomeページを作成
      return {
        default: {
          name: "Welcome",
          template:
            '<div class="text-center py-8"><h1 class="text-2xl font-bold">Welcome to Vidays</h1><p class="text-gray-600 mt-2">Page: {{ $page.component }}</p></div>',
          layout: Layout,
        },
      };
    }
  },
  setup({ el, App, props, plugin }) {
    console.log("Setting up Inertia app with props:", props);
    const app = createApp({ render: () => h(App, props) });
    app.use(plugin);

    // グローバルプロパティとしてrouteを設定
    app.config.globalProperties.route = route;

    app.mount(el);
    console.log("Inertia app mounted");
  },
  page: initialPage,
  progress: {
    color: "#4B5563",
  },
});
