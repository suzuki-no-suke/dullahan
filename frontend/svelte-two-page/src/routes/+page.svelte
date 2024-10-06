<script lang="ts">
    import Breakpoints from "svelte-breakpoints";

    const mediaQueries = {
        small: '(min-width: 0px)',
        medium: '(min-width: 767px)',
        large: '(min-wdith: 1024px)',
    };

    const history = [
        {}
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
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td></td>
                    </tr>
                </tbody>
                {/snippet}

                {#snippet medium()}
                <thead>
                    <tr>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td></td>
                    </tr>
                </tbody>
                {/snippet}

                {#snippet large()}
                <thead>
                    <tr>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td></td>
                    </tr>
                </tbody>
                {/snippet}
            </Breakpoints>
        </table>
    </div>
</div>