<script lang="ts">
    import "../app.css";
    import { AppBar } from "@skeletonlabs/skeleton";
    import { Hamburger } from 'svelte-hamburgers';

    let open: Boolean;
</script>

<AppBar class="sticky top-0 left-0 h-15 w-screen">
    <svelte:fragment slot="lead">
        <Hamburger bind:open type="squeeze" />
    </svelte:fragment>
</AppBar>

{#if open}
<div class="fixed top-30 left-0 w-64 h-screen">
    <ul>
        <li><a href="/history">History</a></li>
        <li>Create New Chat</li>
    </ul>
</div>
{/if}

<slot></slot>