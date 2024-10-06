flowbite svelte
=================


## setup

https://flowbite-svelte.com/docs/pages/quickstart

```
npx svelte-add@latest tailwindcss
npm install
npm install flowbite-svelte flowbite
npm install flowbite-svelte-icons
```

icons は optional

### configuration
tailwind.config.ts

```
import type { Config } from 'tailwindcss';
import flowbitePlugin from 'flowbite/plugin'

export default {
  content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],
  darkMode: 'selector',
  theme: {
    extend: {
      colors: {
        // flowbite-svelte
        primary: {
          50: '#FFF5F2',
          100: '#FFF1EE',
          200: '#FFE4DE',
          300: '#FFD5CC',
          400: '#FFBCAD',
          500: '#FE795D',
          600: '#EF562F',
          700: '#EB4F27',
          800: '#CC4522',
          900: '#A5371B'
        }
      }
    }
  },
  plugins: [flowbitePlugin]
} as Config;
```


