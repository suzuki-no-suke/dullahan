# note

## install

### skeleton

https://www.skeleton.dev/docs/get-started

install skeleton & tailwind
```
npm i @skeletonlabs/skeleton @skeletonlabs/tw-plugin
npx svelte-add@latest tailwindcss
npm install
npm add @types/node

```

overwrite tailwind.config.js
```

import { join } from 'path';
import type { Config } from 'tailwindcss';

// 1. Import the Skeleton plugin
import { skeleton } from '@skeletonlabs/tw-plugin';

const config = {
	// 2. Opt for dark mode to be handled via the class method
	darkMode: 'class',
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		// 3. Append the path to the Skeleton package
		join(require.resolve(
			'@skeletonlabs/skeleton'),
			'../**/*.{html,js,svelte,ts}'
		)
	],
	theme: {
		extend: {},
	},
	plugins: [
		// 4. Append the Skeleton plugin (after other plugins)
		skeleton
	]
} satisfies Config;

export default config;
```

apply theme @ tailwind.config.ts
```ts
plugins: [
	skeleton({
		themes: { preset: [ "wintry" ] }
	})
]
```

and app.html
```html
<body data-theme="wintry">
```

### components

npm i svelte-hamburgers


