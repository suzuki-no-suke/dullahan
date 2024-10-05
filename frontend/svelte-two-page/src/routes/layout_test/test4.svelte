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

    let div_height = 300;
    $: console.log("height : ", div_height);

    function add_height() {
        div_height += 50;
    }
    function del_height() {
        div_height -= 50;
        if (div_height < 100){
            div_height = 100;
        }
    }

</script>


<div class="bg-gray-500">
    <!-- top menu -->
    <div class="bg-blue-400 fixed top-0 w-full">
        <h1>top yade</h1>
        <div class="bg-blue-100">
            <button on:click={add_msg_test}>追加やで</button>
        </div>
        <div class="bg-green-100">
            <button on:click={add_height}>高さ増える</button>
            <button on:click={del_height}>高さ減る</button>
        </div>
    </div>

    <!-- middle - chat area -->
    <div class="bg-green-600" bind:clientHeight={div_height}>
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
        <div>
            <p>{div_height}</p>
        </div>
    </div>

    <!-- bottom chat input -->
    <div class="bg-blue-200 fixed bottom-0 w-full">
        <button on:click={toggle_bottom}>閉じたり開いたり</button>
        {#if bottom_open}
        <div class="bg-blue-100 h-12">
            <button on:click={add_msg_test}>追加やで</button>
        </div>
        {/if}
    </div>
</div>
