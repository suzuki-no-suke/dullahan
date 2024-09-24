<script type="ts">
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from 'svelte';

    let bots = [];

    onMount(async () => {
        const response = await fetch(`${DULLAHAN_URL}/bots/list`);
        bots = await response.json();
    });
</script>

<ul>
    <li><a href="/"> Toppage </a></li>
    <li><a href="/history"> Chat History </a></li>
    <li><a href="/chat">New chat</a></li>
    <li><a href="/bots">Configure bot</a></li>
</ul>

<a href="/bots/create">作成する</a>

{#each bots as bot}
    <li><a href="/bots/{bot.botname}">{bot.botname}</a></li> <!-- bot.name は取得したデータのプロパティ名に応じて変更してください -->
{/each}
