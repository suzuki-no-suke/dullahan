<script lang="ts">
    import { base } from "$app/paths";
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from 'svelte';

    let chatHistory: any[] = [];
    onMount(async () => {
        const response = await fetch(`${DULLAHAN_URL}/chatlist`);
        chatHistory = await response.json();
    });

    let openHamberger = false;
    function toggleHamburger() {
        openHamberger = !openHamberger;
    };
</script>

<!-- whole body -->
<div class="bg-gray-800">
    <!-- top menu-->
    <div class="fixed top-0 w-screen h-8 flex bg-blue-400">
        <div class="basis-1/6 align-middle text-center"><button on:click={toggleHamburger}>(h)</button></div>
        <div class="flex-auto grow justify-center align-middle text-left">Chat History (Top)</div>
    </div>
    
    <!-- left side drawoer -->
    {#if openHamberger}
    <div class="fixed left-0 top-0 bg-gray-100">
        <div class="w-1/6 text-center">
            <div class="align-left h-8"><button on:click={toggleHamburger}>(h)</button></div>
        </div>
        <ul>
            <li><a href="/">History (Top)</a></li>
            <li>new chat</li>
        </ul>
    </div>
    {/if}

    <!-- chat history table -->
    <div class="bg-gray-50 mt-8">
        <div class="flex">
            <p>display in ...</p>
            <p class="visible md:invisible xl:invisible">small...</p>
            <p class="invisible md:visible xl:invisible">medium...</p>
            <p class="invisible md:invisible xl:visible">large...</p>
            <p>mode.</p>
        </div>

        <div class="block">
            <table class="w-screen">
                <thead>
                    <tr>
                        <th>状態</th>
                        <th>タイトル</th>
                        <th class="hidden md:table-cell">最終更新</th>
                        <th class="hidden xl:table-cell">作成時刻</th>
                        <th class="hidden md:table-cell">サマリー</th>
                    </tr>
                </thead>
                <tbody>
                    {#each chatHistory as hist}
                    <tr>
                        <td>{hist.chat_status}</td>
                        <td><a href="{base}/chat/{hist.history_id}">{hist.title}</a></td>
                        <td class="hidden md:table-cell">{hist.updated_at}</td>
                        <td class="hidden xl:table-cell">{hist.created_at}</td>
                        <td class="hidden md:table-cell">{hist.summary}</td>
                    </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>