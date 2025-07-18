import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";
import { resolvePageComponent } from "./utils/resolvePageComponent";
import Layout from "./layouts/Layout.vue";
import "./app.css";

createInertiaApp({
  resolve: async (name) => {
    const page = await resolvePageComponent(
      name,
      import.meta.glob("./pages/**/*.vue")
    );
    page.default.layout = page.default.layout || Layout;
    return page;
  },
  setup({ el, App, props, plugin }) {
    const app = createApp({ render: () => h(App, props) });
    app.use(plugin);
    app.mount(el);
  },
  progress: {
    color: "#4B5563",
  },
});
