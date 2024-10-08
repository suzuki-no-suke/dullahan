<script lang="ts">
    import { base } from "$app/paths";
    import { createChat } from "$lib/create_chat";
    import { goto } from "$app/navigation";

    let openHamberger = false;
    function toggleHamburger() {
        openHamberger = !openHamberger;
    };

    
    let message;
    let create_disabled = false;
    const create_chat = async () => {
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

<!-- whole body -->
<div class="bg-gray-800">
    <!-- top menu-->
    <div class="fixed top-0 w-screen h-8 flex bg-blue-400">
        <div class="basis-1/6 align-middle text-center"><button on:click={toggleHamburger}>(h)</button></div>
        <div class="flex-auto grow justify-center align-middle text-left">Chat History</div>
    </div>
    
    <!-- left side drawoer -->
    {#if openHamberger}
    <div class="fixed left-0 top-0 bg-gray-100 grid w-1/4">
        <div class="align-middle text-center h-8 grid-row">
            <button on:click={toggleHamburger}>(h)</button>
        </div>
        <div class="align-middle text-center grid-row m-2 p-1">
            <button><a href="{base}/">History (Top)</a></button>
        </div>
        <div class="align-middle text-center grid-row m-2 p-1">
            <button on:click={create_chat}>New chat</button>
        </div>
    </div>
    {/if}

    <!-- large create chat button -->
    <div class="mt-8 bg-slate-100">
        <button class="text-2xl m-2 p-1 border rounded-lg bg-green-200" on:click={create_chat}>Create New Chat</button>
    </div>
</div>
