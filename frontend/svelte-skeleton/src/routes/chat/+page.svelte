<script lang="ts">
    import { base } from "$app/paths";
    import { goto } from '$app/navigation';
    import { createChat } from '$lib/create_chat';
    import { getContext } from "svelte";
    import { onMount } from "svelte";

    let create_disabled = false;
    let message = getContext('message');

    onMount(() => {
        message = "";
    })

    const start_chat = async () => {
        create_disabled = true;

        const create_result = await createChat();

        message = create_result.message;

        if (create_result.result) {
            const chatId = create_result.history_id;
            goto(`${base}/chat/${chatId}`);
        } else {
            create_disabled = false;
        }
    };
</script>


<button id="start_chat" on:click={start_chat} disabled={create_disabled}>チャットを開始する</button>
