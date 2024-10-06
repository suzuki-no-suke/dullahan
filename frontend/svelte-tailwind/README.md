Svelte-Tailwind Frontend Sample
=================================

## install tailwindcss

https://tailwindcss.com/docs/guides/sveltekit

```
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

update svelte.convig.js

```
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter()
  },
  preprocess: vitePreprocess()
};
export default config;
```

あれ、もう追加されてた

tailwind.config.js
content を上書き
```
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
}
```

src/app.css を作成
```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

src/routes/+layout.svelte を作成し app.css を記入

test and done

