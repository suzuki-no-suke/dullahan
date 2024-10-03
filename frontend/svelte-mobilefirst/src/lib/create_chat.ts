import { DULLAHAN_URL } from "$lib/constants";
export async function createChat() {
    let message: string = "";
    let history_id: string = "";
    let result: boolean = false;

    try {
        const response = await fetch(`${DULLAHAN_URL}/v1/chat/history`, {
            method: 'GET',
        });

        if (!response.ok) {
            message = "failed to create history";

            return { message, history_id, result };
        }

        const data = await response.json();
        const chatId = data.history_id;

        message = "successfully create new chat";
        history_id = chatId;
        result = true;
    } catch (error) {
        console.error(error);
        message = "failed to create on history" + {error};
        result = false;
    }
    
    return { message, history_id, result }; // 複数の値をオブジェクトとして返す
}
