export function load({ params }){
    const { botname } = params;
    return {
        botname
    };
}

export const prerender = false;
export const ssr = false;