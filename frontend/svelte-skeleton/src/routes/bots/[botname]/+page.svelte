<script lang="ts">
    import { base } from "$app/paths";
    import { DULLAHAN_URL } from "$lib/constants";
    import { onMount } from 'svelte'; // 追加

    export let data;

    let botname = '';
    let useful_when = '';
    let description = '';
    const supported_message_version = ['v1'];
    let module_filename = '';
    let classname = '';
    let message = "waiting for update";

    // 追加: APIを呼び出してbot情報を取得する関数
    const fetchBotInfo = async (route_botname: string) => {
        const response = await fetch(`${DULLAHAN_URL}/bots/edit/${route_botname}`);
        if (!response.ok) {
            message = "error fetching bot info";
            return;
        }
        try {
            const data = await response.json();
            // 取得したデータを変数に設定
            botname = data.botname;
            useful_when = data.useful_when;
            description = data.description;
            module_filename = data.module_filename;
            classname = data.classname;
        } catch {
            message = "error on parse response";
        }
    };

    onMount(() => {
        fetchBotInfo(data.botname);
    });

    const submitForm = async () => {
        const response = await fetch(`${DULLAHAN_URL}/bots/edit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                botname,
                useful_when,
                description,
                supported_message_version,
                module_filename,
                classname,
            }),
        });
        console.log(`send bot config : ${botname}`);
        // Handle response
        if (!response.ok) {
            message = "error on sending message";
        }
        try {
            const parsed = await response.json();
            message = parsed.message;
        } catch {
            message = "error on parse response";
        }
    };

</script>


<form on:submit|preventDefault={submitForm}>
    <label>
        Bot Name:
        <input type="text" value={botname} readonly/>
    </label>
    <br/>
    <label>
        Useful When:
        <input type="text" bind:value={useful_when} required />
    </label>
    <br/>
    <label>
        Description:
        <textarea bind:value={description} required></textarea>
    </label>
    <br/>
    <label>
        Module Filename:
        <input type="text" bind:value={module_filename} required />
    </label>
    <br/>
    <label>
        Class Name:
        <input type="text" bind:value={classname} required />
    </label>
    <br/>
    <button type="submit">Update</button>
</form>
