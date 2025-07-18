export async function resolvePageComponent(name, pages) {
  const page = pages[`./pages/${name}.vue`];
  if (!page) {
    throw new Error(`Page not found: ${name}`);
  }
  return page();
}
