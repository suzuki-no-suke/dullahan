<script type="ts">
    import { base } from "$app/paths";
    import { onMount } from 'svelte';
    import { fetchBots } from '$lib/load_bots';

    let bots = [];

    onMount(async () => {
        bots = await fetchBots();
    });
</script>

<div class="flex-row">
{#if bots && bots.length > 0}
    <ul class="list">
        {#each bots as bot}
            <li><a href="{base}/bots/{bot.botname}">{bot.botname}</a></li> <!-- bot.name は取得したデータのプロパティ名に応じて変更してください -->
        {/each}
    </ul>
{:else}
    <p>No bots registered</p>
{/if}
</div>