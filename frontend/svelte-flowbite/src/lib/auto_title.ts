import { DULLAHAN_URL } from "$lib/constants";
export async function autoTitle(history_id) {
    await fetch(`${DULLAHAN_URL}/v1/chat/history/auto_title?history_id=${history_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Title and summary updated:", data);

        return {
            status_message: "Title and summary updated",
            chat_title: data.title,
            chat_summary: data.summary,
        }
    })
    .catch(error => {
        console.error("Error on update title and summary :", error);
        return {
            status_message: "Title and summary updated",
            chat_title: "---",
            chat_summary: "---",
        }
    });
};
