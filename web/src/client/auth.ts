import * as requests from '@/client/requests'

type LogInRequest = {
    email: string;
    password_plaintext: string;
};
export function log_in({username_or_email, password_plaintext}: LogInRequest) : Promise<Response> {
    return requests.post('/auth/login', {body: { username_or_email, password_plaintext }});
}

export function log_out() : Promise<Response> {
    return requests.post('/auth/logout');
}
