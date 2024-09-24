<script lang="ts">
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from 'svelte';

    let chatHistory = [];

    onMount(async () => {
        const response = await fetch(`${DULLAHAN_URL}/chatlist`);
        chatHistory = await response.json();
    });
</script>

<ul>
    <li><a href="/"> Toppage </a></li>
    <li><a href="/history"> Chat History </a></li>
    <li><a href="/chat">New chat</a></li>
    <li><a href="/bots">Configure bot</a></li>
</ul>

<ul>
    {#each chatHistory as chat}
        <li>({chat.chat_status}) <a href="/chat/{chat.history_id}">{chat.title}</a></li>
    {/each}
</ul>

