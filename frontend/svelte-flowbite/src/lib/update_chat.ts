import { DULLAHAN_URL } from "$lib/constants";

export async function updateTitleAndSummary(history_id, chat_title, chat_summary) {
    await fetch(`${DULLAHAN_URL}/v1/chat/history?history_id=${history_id}&title=${encodeURIComponent(chat_title)}&summary=${encodeURIComponent(chat_summary)}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Title and summary updated:", data);
        return {
            status_message: "Title and summary updated" 
        };
    })
    .catch(error => {
        console.error("Error on update title and summary :", error);
        return {
            status_message: "Error on update title and summary" 
        };
    });
};
