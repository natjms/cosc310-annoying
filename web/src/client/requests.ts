import { LOCALSTORAGE_LOGOUT_FLAG, LOCALSTORAGE_TOKEN_KEY } from '@/utils/security'

enum HTTPMethod {
    POST = 'POST',
    GET = 'GET',
    PATCH = 'PATCH',
    DELETE = 'DELETE',
    PUT = 'PUT',
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function api_path(path: string) : string {
    let trimmed_path = path;
    if (trimmed_path[0] === '/') {
        trimmed_path = trimmed_path.substring(1);
    }

    let trimmed_base_url = API_BASE_URL;
    if (trimmed_base_url[trimmed_base_url.length - 1] == '/') {
        trimmed_base_url = trimmed_base_url.substring(0, trimmed_base_url.length - 1);
    }

    return `${trimmed_base_url}/${trimmed_path}`;
}

function base_request(method: HTTPMethod, path: string, body: object, query: object) : Promise<Response> {
    let options = {method, headers: {}};
    let full_path = path;

    if (body !== undefined) {
        options.body = JSON.stringify(body);
        options.headers = { 'Content-Type': 'application/json' };
    }

    if (query !== undefined) {
        let params = new URLSearchParams();
        for (let key in query) {
            params.append(key, query[key]);
        }
        full_path += `?${params.toString()}`;
    }

    if (localStorage.getItem(LOCALSTORAGE_TOKEN_KEY) !== null) {
        options.headers['Authorization'] = `Bearer ${localStorage.getItem(LOCALSTORAGE_TOKEN_KEY)}`;
    }

    return fetch(api_path(full_path), options)
        .then(response => {
            if (repsponse.status == 401) {
                localStorage.setItem(LOCALSTORAGE_LOGOUT_FLAG, 'true');
            }

            return response;
        });
}

export function get(path: string, data?: {body: object, query: object}) : Promise<Response> {
    return base_request(HTTPMethod.GET, path, data?.body, data?.query);
}

export function post(path: string, data?: {body: object, query: object}) : Promise<Response> {
    return base_request(HTTPMethod.POST, path, data?.body, data?.query);
}

export function put<T>(path: string, data?: {body: object, query: object}) : Promise<Response> {
    return base_request(HTTPMethod.PUT, path, data?.body, data?.query);
}

export function patch(path: string, data?: {body: object, query: object}) : Promise<Response> {
    return base_request(HTTPMethod.PATCH, path, data?.body, data?.query);
}

export function delete_(path: string, data?: {body: object, query: object}) : Promise<Response> {
    return base_request(HTTPMethod.DELETE, path, data?.body, data?.query);
}
