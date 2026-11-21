import * as requests from '@/client/requests'

export type User = {
    id: string;
    username: string;
    email: string;
};

export function get_user(id: string) : Promise<Response> {
    return requests.get(`/users/${id}`);
}

type CreateUserRequest = {
    username: string,
    email: string,
    password_plaintext: string,
};
export function create_user({ username, email, password_plaintext }: CreateUserRequest) : Promise<Response> {
    return requests.post('/users/', { body: { username, email, password_plaintext } });
}
