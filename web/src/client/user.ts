import * as requests from '@/client/requests'

export type User = {
    id: string;
    username: string;
    email: string;
};

export function get_user(id: string) : Promise<Response> {
    return requests.get(`/users/${id}`);
}
