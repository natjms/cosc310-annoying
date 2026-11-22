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
export function create_user(role: string, { username, email, password_plaintext }: CreateUserRequest) : Promise<Response> {
    return requests.post(`/users/?role=${role}`, { body: { username, email, password_plaintext } });
}

type UpdateUserRequest = {
    username: string,
    email: string,
    password_plaintext: string,
};
export function update_user(user_id, { username, email, password_plaintext }: UpdateUserRequest) : Promise<Response> {
    return requests.patch(`/users/${user_id}`, { body: { username, email, password_plaintext } });
}
