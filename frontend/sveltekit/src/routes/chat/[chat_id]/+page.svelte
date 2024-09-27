<script lang="ts">
    import { base } from "$app/paths";
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from "svelte";

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

            const bot_list_response = await fetch(`${DULLAHAN_URL}/bots/list`);
            botlist = await bot_list_response.json();
        });

    let botname = ""; // 新規変数
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

    function updateTitleAndSumary() {
        status_message = "Updating title and summary";
        console.log(`input title is ${chat_title}, summary is ${chat_summary}`);

        fetch(`${DULLAHAN_URL}/v1/chat/history?history_id=${data.chat_id}&title=${encodeURIComponent(chat_title)}&summary=${encodeURIComponent(chat_summary)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Title and summary updated:", data);
            status_message = "Title and summary updated";
        })
        .catch(error => {
            console.error("Error on update title and summary :", error);
            status_message = "Error on update title and summary";
        });
    };

    function autoTitle() {
        status_message = "Updating title and summary";
        
        fetch(`${DULLAHAN_URL}/v1/chat/history/auto_title?history_id=${data.chat_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Title and summary updated:", data);
            status_message = "Title and summary updated";

            chat_title = data.title;
            chat_summary = data.summary;
        })
        .catch(error => {
            console.error("Error on update title and summary :", error);
            status_message = "Error on update title and summary";
        });
    };
</script>

<ul>
    <li><a href="{base}/"> Toppage </a></li>
    <li><a href="{base}/history"> Chat History </a></li>
    <li><a href="{base}/chat">New chat</a></li>
    <li><a href="{base}/bots">Configure bot</a></li>
</ul>

<h1>Chat</h1>

<p>current sutatus : {status_message}</p>

<p>chat status : {status}</p>

<label>
title : 
<input type="text" bind:value={chat_title}/><br/>
</label>

<label>
summary : 
<textarea bind:value={chat_summary}></textarea>
</label>

<button on:click={updateTitleAndSumary}>更新</button>

<button on:click={autoTitle}>自動タイトル設定</button>

<!-- チャット履歴を表示 -->
{#if chat_messages && chat_messages.length > 0}
<ul>
    {#each chat_messages as message}
        <li>
            <strong>{message.sender_type}:</strong> {message.content} <br />
            <small>{message.time} - {message.botname} ({message.agent})</small>
        </li>
    {/each}
</ul>
{:else}
<p>No Message</p>
{/if}

<select bind:value={selected_bot}>
    {#each botlist as bot}
        <option value={bot.botname}>{bot.botname}</option>
    {/each}
</select>
<input type="text" bind:value={content} placeholder="メッセージを入力..." />
<button on:click={sendMessage}>送信</button>

