<script>
    import "../app.css";
    import { base } from "$app/paths";
    import { AppBar } from '@skeletonlabs/skeleton';
    import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
    import { createChat } from "$lib/create_chat";
    import { goto } from "$app/navigation";

    let create_disabled = false;
    export let message = "";

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

    $: outerWidth = 0;
    $: innerWidth = 0;
    $: outerHeight = 0;
    $: innerHeight = 0;
</script>

<svelte:window bind:innerWidth bind:outerWidth bind:innerHeight bind:outerHeight />

<AppBar>
	<svelte:fragment slot="lead">
        <button type="button" class="btn variant-filled"><a href="{base}/">Toppage</a></button>
    </svelte:fragment>
    <button type="button" class="btn variant-filled" on:click={create_chat} disable={create_disabled}>New Chat</button>
    <button type="button" class="btn variant-filled"><a href="{base}/history">Chat History</a></button>
    <svelte:fragment slot="trail">
        <button type="button" class="btn variant-filled"><a href="{base}/bots">Bots</a></button>
    </svelte:fragment>
</AppBar>

<div class="flex">
    <AppRail class="flex-none">
        <svelte:fragment slot="lead">
            <AppRailAnchor on:click={create_chat} disable={create_disabled}>New Chat</AppRailAnchor>
            <AppRailAnchor href="{base}/history">Chat History</AppRailAnchor>
            <AppRailAnchor href="{base}/bots">Edit bots</AppRailAnchor>
        </svelte:fragment>

        <svelte:fragment slot="trail">
            <AppRailTile>
                <p>by Svelte Skeleton</p>
            </AppRailTile>
            <AppRailTile>
                <p>inner W {innerWidth}px x H {innerHeight}px</p>
            </AppRailTile>
            <AppRailTile>
                <p>outer W {outerWidth}px x H {outerHeight}px</p>
            </AppRailTile>
        </svelte:fragment>
    </AppRail>

    <div class="grid grid-flow-row-dense place-content-center place-items-center flex-1">
        <p>{message}</p>
        <div class="grid-flow-col auto-col-max">
            <slot></slot>
        </div>
    </div>
</div>
