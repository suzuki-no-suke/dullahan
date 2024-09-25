export function load({ params }){
    const { chat_id } = params;
    return {
        chat_id
    };
}

export const prerender = false;
export const ssr = false;
