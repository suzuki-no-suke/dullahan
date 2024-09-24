<script lang="ts">
    import { DULLAHAN_URL } from "$lib/constants";

    let botname = '';
    let useful_when = '';
    let description = '';
    const supported_message_version = ['v1'];
    let module_filename = '';
    let classname = '';

    let message="waiting for input";

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
        console.log("send bot config {botname}")
        // Handle response
        if (!response.ok) {
            message = "error on sending message";
        }
        try {
            const parsed = await response.json();
            message = parsed.message;
        } catch  {
            message = "error  on parse response"
        }
    };
</script>

<ul>
    <li><a href="/"> Toppage </a></li>
    <li><a href="/history"> Chat History </a></li>
    <li><a href="/chat">New chat</a></li>
    <li><a href="/bots">Configure bot</a></li>
</ul>

<p>{message}</p>

<form on:submit|preventDefault={submitForm}>
    <label>
        Bot Name:
        <input type="text" bind:value={botname} required />
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
    <button type="submit">Submit</button>
</form>



