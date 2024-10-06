<script lang="ts">
    import { base } from "$app/paths";
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from 'svelte';
    import { Paginator, Table } from "@skeletonlabs/skeleton";

    let chatHistory: any[] = [];

    let pageSett = {
        page: 0,
        limit: 7,
        size: chatHistory.length,
        amounts: [5, 7, 10]
    } satisfies PaginationSettings;

    onMount(async () => {
        const response = await fetch(`${DULLAHAN_URL}/chatlist`);
        chatHistory = await response.json();
        print(chatHistory);
    });

    $: paginatedSource = chatHistory.slice(
        pageSett.page * pageSett.limit,
        pageSett.page * pageSett.limit + pageSett.limit
    );

    $: pageSett.size = chatHistory.length || 0;

    $: console.log("paginate source updated : ", paginatedSource);
    $: console.log("paginate original length : ", chatHistory.length);

    function onPageChange(e: CustomEvent): void {
        console.log('Paginator - event:page', e);
    }
</script>

{#if Array.isArray(chatHistory) && chatHistory.length > 0}
<div class="table-container">
<table class="table table-hover">
    <thead>
        <tr>
            <th>タイトル</th>
            <th>チャットステータス</th>
            <th>概要</th>
        </tr>
    </thead>
    <tbody>
        {#each paginatedSource as chat}
            <tr>
                <td><a href="{base}/chat/{chat.history_id}">{chat.title}</a></td>
                <td>{chat.chat_status}</td>
                <td>{chat.summary}</td>
            </tr>
        {/each}
    </tbody>
</table>
</div>

<Paginator
    bind:settings={pageSett}
    showFirstLastButtons="{true}"
    showPreviousNextButtons="{true}"
    on:page={onPageChange}
/>
{:else}
    <p>History data loading ...</p>
{/if}
