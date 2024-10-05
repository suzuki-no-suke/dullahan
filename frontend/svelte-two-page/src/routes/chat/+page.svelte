<script lang="ts">
    const history_text = "test yade";

    let menu_open: boolean = false;
    let bottom_open: boolean = true;

    let demo_message = [
        { agent: "human", content: "hello hou are you ?"},
        { agent: "chatbot", content: "I'm fine, And you ?"},
    ];

    function add_msg_test() {
        demo_message.push({ agent: "chatbot", content: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passa"});
        demo_message.push({ agent: "human", content: "Me too !"});
        demo_message = demo_message;
    }
    
    const bots = [
        "bot1",
        "bot2",
    ]

    function onToggleMenu () {
        menu_open = !menu_open;
    }
    function onToggleBottom(){
        bottom_open = !bottom_open;
    }
</script>

<div>
    <!-- leftside nav menu  -->
    {#if menu_open}
    <div class="fixed top-12 z-10 bg-blue-100 p-2 w-36">
        <div>
            <ul>
                <li class="p-2">menu item</li>
                <li class="p-2">menu item 2</li>
                <li class="p-2">menu item 3</li>
                <li class="p-2">menu item 4</li>
                <li class="p-2">menu item 5</li>
            </ul>
        </div>
    </div>
    {/if}

    <!-- sticky top menu -->
    <div class="bg-blue-400 flex fixed top-0 z-10 h-12 w-screen">
        <button on:click={onToggleMenu}>(hamburger)</button>
        <h1>{history_text}</h1>
        <span>(left menu icon)</span>
    </div>

    <!-- chat display area -->
    <div class="top-12 bottom-36 relative">
        <div class="w-full">
            <div class="grid grid-cols-1 m-2 gap-2">
                {#each demo_message as message}
                <div class="col-span-full gap-1 rounded-r-xl rounded-bl-xl border px-2 m-1 bg-green-100">
                    <div>
                        <span class="font-bold">{message.agent}</span>
                        <span>(when)</span>
                    </div>
                    <div>
                        <span>{message.content}</span>
                    </div>
                </div>
                {/each}
            </div>
        </div>
        
        <!-- bottom filler -->
        {#if bottom_open}
        <div class="h-36 bottom-36 bg-blue-800">
            <p>copyright by yosho-naka.ltd</p>
        </div>
        {/if}
    </div>

    <!-- sticky bottom chat input -->
    <div class="fixed grid grid-cols-1 w-screen bottom-0 z-20 h-36">
        <div class="cols-auto justify-self-end">
            <span class="bg-blue-100"><a href="#" on:click={onToggleBottom}>^^ tip up ^^</a></span>
        </div>
        {#if bottom_open}
        <div class="bg-blue-400 cols-auto">
            <form>
                <div class="basis-1 flex flex-row">
                    <div class="basis-1/2">
                        <label for="bots">botname : 
                            <select id="bots">
                                {#each bots as b}
                                <option value={b}>
                                    {b}
                                </option>
                                {/each}
                            </select>
                        </label>
                    </div>
                    <div class="basis-1/2 justify-right">
                        <span>(last_update_at)</span>
                    </div>
                </div>
                <div class="basis-1">
                    <textarea></textarea>
                    <button type="submit" on:click={add_msg_test}>
                        送信
                    </button>
                </div>
            </form>
        </div>
        {/if}
    </div>
</div>