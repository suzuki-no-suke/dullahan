<script lang="ts">
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
        <div class="flex-auto grow justify-center align-middle text-left">Chat History</div>
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

    <!-- large create chat button -->
    <div class="mt-8 bg-slate-100">
        <button class="text-2xl m-2 p-1 border rounded-lg bg-green-200">Create New Chat</button>
    </div>
</div>
