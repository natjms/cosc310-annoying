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

function base_request<T>(method: HTTPMethod, path: string, body: object, query: object) : Promise<T> {
    let options = {method};
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

    return fetch(api_path(full_path), options)
        .then(response => response.json());
}

export function get<T>(path: string, data?: {body: object, query: object}) : Promise<T> {
    return base_request<T>(HTTPMethod.GET, path, data?.body, data?.query);
}

export function post<T>(path: string, data?: {body: object, query: object}) : Promise<T> {
    return base_request<T>(HTTPMethod.POST, path, data?.body, data?.query);
}

export function put<T>(path: string, data?: {body: object, query: object}) : Promise<T> {
    return base_request<T>(HTTPMethod.PUT, path, data?.body, data?.query);
}

export function patch<T>(path: string, data?: {body: object, query: object}) : Promise<T> {
    return base_request<T>(HTTPMethod.PATCH, path, data?.body, data?.query);
}

export function delete_(path: string, data?: {body: object, query: object}) : Promise {
    return base_request(HTTPMethod.DELETE, path, data?.body, data?.query);
}
