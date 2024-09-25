<script type="ts">
    import { base } from "$app/paths";
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from 'svelte';

    let bots = [];

    onMount(async () => {
        const response = await fetch(`${DULLAHAN_URL}/bots/list`);
        bots = await response.json();
    });
</script>

<ul>
    <li><a href="{base}/"> Toppage </a></li>
    <li><a href="{base}/history"> Chat History </a></li>
    <li><a href="{base}/chat">New chat</a></li>
    <li><a href="{base}/bots">Configure bot</a></li>
</ul>

<a href="{base}/bots/create">作成する</a>

{#each bots as bot}
    <li><a href="{base}/bots/{bot.botname}">{bot.botname}</a></li> <!-- bot.name は取得したデータのプロパティ名に応じて変更してください -->
{/each}
