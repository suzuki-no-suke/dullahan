<script lang="ts">
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
    }

    let bottom_open = false;
    function toggle_bottom() {
        bottom_open = !bottom_open;
    }
</script>


<div class="bg-gray-500 grid grid-rows-12">
    <!-- top menu -->
    <div class="bg-blue-400 row-start-1 row-span-1">
        <h1>top yade</h1>
        <div class="bg-blue-100">
            <button on:click={add_msg_test}>追加やで</button>
        </div>
    </div>

    <!-- middle - chat area -->
    <div class="bg-green-600 row-start-2 row-end-11 row-span-auto">
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
    <div class="bg-blue-200 w-full row-end-12 row-span-1">
        <button on:click={toggle_bottom}>閉じたり開いたり</button>
        {#if bottom_open}
        <div class="bg-blue-100 h-12">
            <button on:click={add_msg_test}>追加やで</button>
        </div>
        {/if}
    </div>
</div>
