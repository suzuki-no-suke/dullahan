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

        resize_center();
    };

    let bottom_open = false;
    function toggle_bottom() {
        bottom_open = !bottom_open;
    };

    let top_menu;
    let center_content;
    let bottom_menu;

    let win_height;

    function resize_center(){
        if (!top_menu || !center_content || !bottom_menu) {
            console.debug("Failed find three contents !", {top_menu, center_content, bottom_menu});
            return;
        }
        //console.debug("three : ", {top_menu, center_content, bottom_menu});
        console.log("bottom : ", bottom_menu);
        console.log("- attrib : ", bottom_menu.attributes);
        console.log("- style : ", bottom_menu.style);
        console.log("- client top : ", bottom_menu.clientTop);
        console.log("- client height : ", bottom_menu.clientHeight);
        console.log("- offset top : ", bottom_menu.offsetTop);
        console.log("window height : ", win_height);
        
        // console.log("top : ", top_menu.getBoundClientRect());
        // console.log("center : ", center_content.getBoundClientRect());
        // console.log("bottom : ", bottom_menu.getBoundClientRect());
        console.debug(top_menu.offsetTop, " - top - ", top_menu.offsetTop + top_menu.clientHeight);
        console.debug(" --- - ", center_content.offsetTop, " - center - ", center_content.offsetTop + center_content.clientHeight, " - ---");
        console.debug(bottom_menu.offsetTop, " - bottom - ", bottom_menu.offsetTop + bottom_menu.clientHeight);

        center_content.style.marginTop = top_menu.offsetTop + top_menu.clientHeight;
        console.debug("updated : --- - ", center_content.offsetTop, " - center - ", center_content.offsetTop + center_content.clientHeight, " - ---");
    };

    onMount(async () => {
        // resizing process
        resize_center();
    });
</script>

<svelte:window bind:innerHeight={win_height} />

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

    <!-- middle - chat area -->
    <div class="bg-green-600 mt-8 mb-16" id="center_content" bind:this={center_content}>
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
    <div class="bg-blue-200 fixed bottom-0 w-full h-16" id="bottom_menu" bind:this={bottom_menu}>
        <button on:click={toggle_bottom}>閉じたり開いたり</button>
        {#if bottom_open}
        <div class="bg-blue-100 h-12">
            <button on:click={add_msg_test}>追加やで</button>
        </div>
        {/if}
    </div>
</div>
