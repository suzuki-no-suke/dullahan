<script lang="ts">
    import Breakpoints from "svelte-breakpoints";

    const mediaQueries = {
        small: '(min-width: 0px)',
        medium: '(min-width: 767px)',
        large: '(min-wdith: 1024px)',
    };

    interface History {
        history_id: string;
        chat_status: string;
        message_version: string;
        title: string;
        summary: string;
        updated_at: string;
        created_at: string;
    }

    const history: History[] = [
        {history_id: '12345', chat_status: 'in_progress', message_version: 'v1', title: '---', summary: '---', updated_at: "2024-10-01T00:00:00", created_at: "2024-10-01T00:00:00"},
        {history_id: '12346', chat_status: 'waiting', message_version: 'v1', title: '---', summary: '---', updated_at: "2024-10-01T00:00:00", created_at: "2024-10-01T00:00:00"},
        {history_id: '12347', chat_status: 'completed', message_version: 'v1', title: '---', summary: '---', updated_at: "2024-10-01T00:00:00", created_at: "2024-10-01T00:00:00"},
        {history_id: '12348', chat_status: 'in_progress', message_version: 'v1', title: '---', summary: '---', updated_at: "2024-10-01T00:00:00", created_at: "2024-10-01T00:00:00"},
        {history_id: '12349', chat_status: 'in_progress', message_version: 'v1', title: '---', summary: '---', updated_at: "2024-10-01T00:00:00", created_at: "2024-10-01T00:00:00"},
        {history_id: '12340', chat_status: 'in_progress', message_version: 'v1', title: '---', summary: '---', updated_at: "2024-10-01T00:00:00", created_at: "2024-10-01T00:00:00"},
    ];

    let openHamberger = true;
    function toggleHamburger() {
        openHamberger = !openHamberger;
    };
</script>

<!-- whole body -->
<div class="bg-gray-800">
    <!-- top menu-->
    <div class="fixed top-0 w-screen h-8 flex bg-blue-400">
        <div class="basis-1/6 align-middle text-center"><button on:click={toggleHamburger}>(h)</button></div>
        <div class="flex-auto grow justify-center align-middle text-left">Chat History</div>
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

    <!-- chat history table -->
    <div>
        <Breakpoints queries={mediaQueries}>
            {#snippet small()}
                <p>display in small mode</p>                
            {/snippet}
            {#snippet medium()}
                <p>display in medium mode</p>
            {/snippet}
            {#snippet large()}
                <p>display in large mode</p>                
            {/snippet}
        </Breakpoints>
        <table>
            <Breakpoints queries={mediaQueries}>
                {#snippet small()}
                <thead>
                    <tr>
                        <th>状態</th>
                        <th>タイトル</th>
                        <th>最終更新</th>
                    </tr>
                </thead>
                <tbody>
                    {#each history in hist}
                    <tr>
                        <td>{hist.chat_status}</td>
                        <td>{hist.title}</td>
                        <td>{hist.updated_at}</td>
                    </tr>
                    {/each}
                </tbody>
                {/snippet}

                {#snippet medium()}
                <thead>
                    <tr>
                        <th>状態</th>
                        <th>タイトル</th>
                        <th>最終更新</th>
                        <th>サマリー</th>
                    </tr>
                </thead>
                <tbody>
                    {#each history in hist}
                    <tr>
                        <td>{hist.chat_status}</td>
                        <td>{hist.title}</td>
                        <td>{hist.updated_at}</td>
                        <td>{hist.summary}</td>
                    </tr>
                    {/each}
                </tbody>
                {/snippet}

                {#snippet large()}
                <thead>
                    <tr>
                        <th>状態</th>
                        <th>タイトル</th>
                        <th>最終更新</th>
                        <th>作成時刻</th>
                        <th>サマリー</th>
                    </tr>
                </thead>
                <tbody>
                    {#each history in hist}
                    <tr>
                        <td>{hist.chat_status}</td>
                        <td>{hist.title}</td>
                        <td>{hist.updated_at}</td>
                        <td>{hist.created_at}</td>
                        <td>{hist.summary}</td>
                    </tr>
                    {/each}
                </tbody>
                {/snippet}
            </Breakpoints>
        </table>
    </div>
</div>