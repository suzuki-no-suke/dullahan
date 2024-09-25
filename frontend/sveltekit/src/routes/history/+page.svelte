<script lang="ts">
    import { base } from "$app/paths";
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from 'svelte';

    let chatHistory = [];

    onMount(async () => {
        const response = await fetch(`${DULLAHAN_URL}/chatlist`);
        chatHistory = await response.json();
    });
</script>

<ul>
    <li><a href="{base}/"> Toppage </a></li>
    <li><a href="{base}/history"> Chat History </a></li>
    <li><a href="{base}/chat">New chat</a></li>
    <li><a href="{base}/bots">Configure bot</a></li>
</ul>

<ul>
    {#each chatHistory as chat}
        <li>({chat.chat_status}) <a href="{base}/chat/{chat.history_id}">{chat.title}</a></li>
    {/each}
</ul>

