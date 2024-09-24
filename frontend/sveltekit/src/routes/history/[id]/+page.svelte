<script>
    import { page } from '$app/stores';

    export let data = {
        title: "タイトルやで",
        messages: [
            {
                content: "メッセージやで"
            },
            {
                content: "次のメッセージやで"
            }
        ]
    }
</script>

<h1>chat history : {data.title}</h1>
<p>id = {$page.params.id}</p>

<!-- chat history 表示 -->
{#each data.messages as d}
    <h2>who send</h2>
    <p>{d.content}</p>

{/each}
