<script lang="ts">
    import { DULLAHAN_URL } from "$lib/constants";
    import { goto } from '$app/navigation';

    let message = "";
    let create_disabled = false;

    const start_chat = async () => {
        create_disabled = true;

        try {
            // API /v1/chat/history にアクセスしてチャットIDを取得
            const response = await fetch(`${DULLAHAN_URL}/v1/chat/history`, {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('チャットIDの取得に失敗しました');
            }

            const data = await response.json();
            const chatId = data.history_id;

            // /chat/<チャットID> にリダイレクト
            goto(`/chat/${chatId}`);
        } catch (error) {
            console.error(error);
            // エラーハンドリングをここに追加することができます
            create_disabled = false;
        }
    };
</script>

<ul>
    <li><a href="/"> Toppage </a></li>
    <li><a href="/history"> Chat History </a></li>
    <li><a href="/chat">New chat</a></li>
    <li><a href="/bots">Configure bot</a></li>
</ul>

<h1>start chatting</h1>
<p>{message}</p>

<button id="start_chat" on:click={start_chat} disabled={create_disabled}>チャットを開始する</button>