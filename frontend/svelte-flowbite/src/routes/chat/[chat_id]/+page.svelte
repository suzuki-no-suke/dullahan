<script lang="ts">
    import { base } from "$app/paths";
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from "svelte";
    import { fetchBots } from "$lib/load_bots";
    import { autoTitle } from "$lib/auto_title";
    import { updateTitleAndSummary } from "$lib/update_chat";

    export let data;

    let status_message = "waiting for chat";

    let status = "unknown";
    let chat_title = "---";
    let chat_summary = "---";
    let chat_messages: any[] = [];
    let botlist : any[] = [];
    let selected_bot = "";

    // メッセージの型を定義
    interface ChatMessage {
        message_id: string;
        time: string;
        sender_type: string;
        botname: string;
        agent: string;
        content: string;
    }

    onMount(
        async () => {
            const chatId = data.chat_id;
            const response = await fetch(`${DULLAHAN_URL}/v1/chat/history/${chatId}`);
            const response_body = await response.json();
            
            console.log(response_body)

            chat_title = response_body.title;
            chat_summary = response_body.summary;
            chat_messages = response_body.messages || [];

            console.log("message loaded");

            botlist = await fetchBots();
    });

    let content = "";  // 新規変数

    function sendMessage() {
        const newMessage: ChatMessage = {
            message_id: "-----",
            time: new Date().toISOString(),
            sender_type: 'human',
            botname: selected_bot,
            agent: 'sveltekit',
            content: content
        };
        chat_messages.push(newMessage);
        chat_messages = chat_messages;

        const messageData = {
            sender_type: 'human',
            botname: selected_bot,
            agent: 'sveltekit',
            content: content
        };

        fetch(`${DULLAHAN_URL}/v1/chat/send?history_id=${data.chat_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(messageData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Message response:", data);

            // replace user message and add other messages
            if (chat_messages.length > 0) {
                const lastMessage = chat_messages[chat_messages.length - 1];
                if (lastMessage.sender_type === 'human' && lastMessage.content === data.messages[0].content) {
                    chat_messages.pop();
                }
            }

            // 新しいメッセージを追加
            data.messages.forEach(message => {
                chat_messages.push(message);
            });

            chat_messages = chat_messages;
        })
        .catch(error => {
            console.error("Error sending message:", error);
            status_message = "Error sending message: " + error;
        });
    };

    async function updateTitleAndSumary_button() {
        status_message = "Updating title and summary";
        console.log(`input title is ${chat_title}, summary is ${chat_summary}`);

        const result = await updateTitleAndSummary(data.chat_id, chat_title, chat_summary);

        status_message = result.status_message;
    };

    async function autoTitle_button() {
        status_message = "Updating title and summary";
        
        const result = await autoTitle(data.chat_id);

        status_message = result.status_message;
        chat_title = result.chat_title;
        chat_summary = result.chat_summary;
    }
    
    let openHamberger = false;
    function toggleHamburger() {
        openHamberger = !openHamberger;
    };
    
    let bottom_open = false;
    function toggle_bottom() {
        bottom_open = !bottom_open;
    };

    let top_editor_open = false;
    function toggle_top_editor() {
        top_editor_open = !top_editor_open
    }
</script>

<!-- whole body -->
<div class="bg-gray-800">
    <!-- top menu-->
    <div class="fixed top-0 w-screen h-8 flex bg-blue-400">
        <div class="w-1/6 align-middle text-center"><button on:click={toggleHamburger}>(h)</button></div>
        <div class="flex-auto grow justify-center align-middle text-left">Chat History</div>
    </div>

    <!-- left side drawoer -->
    {#if openHamberger}
    <div class="fixed left-0 top-0 bg-gray-100 flex">
        <div>
            <div class="w-1/6 align-middle text-center h-8"><button on:click={toggleHamburger}>(h)</button></div>
        </div>
        <ul class="w-1/6">
            <li><a href="/">History (Top)</a></li>
            <li>new chat</li>
        </ul>
    </div>
    {/if}

    <!-- status bar -->
    <div class="bg-surface-500/30 p-4">
        <h1>Chat</h1>
        <p>chat status : {status}</p>

        <p>current status : {status_message}</p>
    </div>

    <!-- top editor area -->
    <div class="bg-slate-100 p-4 {top_editor_open ? 'flex-box' : 'hidden'}">
        <label>
            title : 
            <input type="text" bind:value={chat_title}/><br/>
            </label>
            
            <label>
            summary : 
            <textarea bind:value={chat_summary}></textarea>
        </label>

        <button on:click={updateTitleAndSumary_button}>更新</button>
        <button on:click={autoTitle_button}>自動タイトル設定</button>
    </div>
    <button on:click={toggle_top_editor}>{top_editor_open ? "閉じる" : "開く"}</button>

    <!-- chat history -->
    <div class="bg-green-600 mt-8 {bottom_open ? 'mb-36' : 'mb-8'}">
    {#if chat_messages && chat_messages.length > 0}
        {#each chat_messages as message}
        <div class="p-4">
            <header class="flex justify-between">
                <strong>{message.agent}</strong> ({message.sender_type})
            </header>

            <div>
                <p>{message.content}</p>
            </div>

            <footer class="flex justify-between">
                <small>{message.time} (botname : {message.botname})</small>
            </footer>
        </div>
        {/each}
    {:else}
        <div class="p-4">
            <p>No Message</p>
        </div>
    {/if}
    </div>

    <!-- prompt input -->
    <div class="bg-blue-200 fixed bottom-0 w-full flex">
        <button class="h-8 justify-end" on:click={toggle_bottom}>閉じたり開いたり</button>
        {#if bottom_open}
        <div class="{bottom_open ? 'h-36' : 'h-8'}">
            <select bind:value={selected_bot}>
                {#each botlist as bot}
                    <option class="input-group-shim" value={bot.botname}>{bot.botname}</option>
                {/each}
            </select>
    
            <textarea
                bind:value={content} placeholder="メッセージを入力..." rows=2
                class="bg-transparent border-0 ring-0"
            />
            <button class="variant-filled-primary" on:click={sendMessage}>送信</button>
        </div>
        {/if}
    </div>
</div>
