import { DULLAHAN_URL } from "$lib/constants";
export async function fetchBots() {
    const response = await fetch(`${DULLAHAN_URL}/bots/list`);
    return await response.json();
}
