<script>
    import { page } from '$app/stores';

    export let data;
    export let params;
</script>

<h1>chatting with {data.title}</h1>
<p>content -> {data.content}</p>

params is now -> {$page.params.botname}