<script lang="ts">
    import { onMount } from "svelte";

    let messages = [
        { agent: "human", content: "hello, world"},
        { agent: "chatbot", content: "hi, i'm fine, and you ?"},
    ]
    function add_msg_test() {
        messages.push({
            agent: "human", content: "this is just a response"
        });
        messages.push({
            agent: "chatbot", content: "this is just a response"
        });
        messages = messages;
    };

    let bottom_open = false;
    function toggle_bottom() {
        bottom_open = !bottom_open;
    };

    const closed_height = 'h-8';
    const open_height = 'h-20';

    const closed_bottom = 'mb-8';
    const open_bottom = 'mb-20';

    let top_menu;
    let center_content;
    let bottom_menu;

    let openHamberger = true;
    function toggleHamburger() {
        openHamberger = !openHamberger;
    }
</script>

<div class="bg-gray-500">
    <!-- top menu -->
    <div class="bg-blue-400 fixed top-0 w-full h-8" id="top_menu" bind:this={top_menu}>
        <div class="flex">
            <h1>top yade</h1>
            <div class="bg-blue-100">
                <button on:click={add_msg_test}>追加やで</button>
            </div>
        </div>
    </div>

    <!-- left side drawoer -->
    {#if openHamberger}
    <div class="sticky left-0 top-0 bg-gray-100">
        <div class="w-1/6 text-center">
            <div class="align-left h-8"><button on:click={toggleHamburger}>(h)</button></div>
        </div>
        <ul>
            <li><a href="/chat">to chat</a></li>
            <li>new chat</li>
            <li><a href="/layout_test">layout</a></li>
        </ul>
    </div>
    {/if}

    <!-- middle - chat area -->
    <div class="bg-green-600 mt-8 {bottom_open ? open_bottom : closed_bottom}" id="center_content" bind:this={center_content}>
        {#each messages as msg}
        <div class="border bg-green-400">
            <div>
                <h2>{msg.agent}</h2>
                <span>(when)</span>
            </div>
            <div>
                <p>
                    {msg.content}
                </p>
            </div>
        </div>
        {/each}
    </div>

    <!-- bottom chat input -->
    <div class="bg-blue-200 fixed bottom-0 w-full {bottom_open ? open_height : closed_height}" id="bottom_menu" bind:this={bottom_menu}>
        <button on:click={toggle_bottom}>閉じたり開いたり</button>
        {#if bottom_open}
        <div class="bg-blue-100 h-12">
            <button on:click={add_msg_test}>追加やで</button>
        </div>
        {/if}
    </div>
</div>
