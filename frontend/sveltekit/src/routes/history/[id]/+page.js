import { error } from '@sveltejs/kit';

export function load({ params }) {
    if (params.id === '12345') {
        return {
            title: "testyade",
            content: "testo yade na"
        };
    }

    error(404, 'Not found');
}