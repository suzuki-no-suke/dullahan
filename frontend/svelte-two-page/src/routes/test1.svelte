<script lang="ts">

    const chat_message_dummy = [
        { id: 1, agent: "human", content: "hello hou are you ?"},
        { id: 2, agent: "chatbot", content: "I'm fine, And you ?"},
        { id: 3, agent: "human", content: "Me too !"},
    ]
    const bots = [
        "bot1",
        "bot2",
    ]
</script>

<!-- whole body -->
<div class="flex h-screen bg-gray-100">
    <!-- leftside menu -->
    <div class="fixed inset-y-0 left-0 transform">
        <div class="flex flex-col h-full">
            <div class="flex items-center justify-between p-4 border-b">
                <div>
                    <button>hamburger</button>
                    <h2>Menu</h2>
                </div>
            </div>
            <nav class="flex-1 p-4">
                <ul class="space-y-2">
                    <li>
                        <a href="/">Chats</a>
                    </li>
                    <li>
                        <a href="/chat">for test</a>
                    </li>
                    <li>
                        <a href="/layout_test">test layout</a>
                    </li>
                    <li>
                        <a href="#">New Chat</a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>

    <!-- stick top bar-->
    <div class="flex flex-col flex-1 lg:ml-72">
        <div class="flex items-center">
            <button class="mr-4 lg:hidden">
                <span class="sr-only">Toggle Menu</span>
            </button>
            <h1 class="text-xl font-bold">Chat app here</h1>
        </div>
    </div>

    <!-- chat message -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
        {#each chat_message_dummy as chat}
        <div class="w-full p-3 rounded-lg">
            <div class="font-bold">
                {chat.agent}
            </div>
            <div class="mt-1 text-gray-800">
                {chat.content}
            </div>
        </div>
        {/each}
    </div>

    <!-- sticky chat input form at bottom -->
    <div class="sticky bottom-0 bg-white p-4 border-t border-gray-200">
        <form class="flex space-x-2">
            <div>
                <select>
                    {#each bots as b}
                    <option value={b}>
                        {b}
                    </option>
                    {/each}
                </select>
                <span>(last_update_at)</span>
            </div>
            <div>
                <textarea></textarea>
                <button type="submit">
                    送信
                </button>
            </div>
        </form>
    </div>
</div>