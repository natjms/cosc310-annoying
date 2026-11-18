import { createContext, useState, Children } from 'react';

export const navigator = createContext(null);

const path_regex = /^\/(?:(?:[A-Za-z_](?:\w)*\/?)|(?:{([A-Za-z_](?:\w)*)}\/?))*$/g
const param_regex = /{[A-Za-z_]\w*}/g

type RouteProps = {
    path: string;
    component: ReactNode;
};

export function Route(props: RouteProps) {
    const {path, component} = props;
    return component;
}

const hash_path = (path: string) => {
    // Stub params
    let hashed_path = path.replaceAll(param_regex, '\\VARIABLE\\');

    // Remove trailing slashes
    if (hashed_path.length > 1 && hashed_path.substring(hashed_path.length - 1) == '/') {
        hashed_path = hashed_path.substring(0, hashed_path.length - 1)
    }

    return hashed_path;
}

type NatsFriendlyRouterProps = {
    children: ReactNode;
};

export function NatsFriendlyRouter(props: NatsFriendlyRouterProps) {
    if (window.location.hash.length === 0) {
        window.location.hash = '#/';
    }

    const url_path = window.location.hash.substring(1);

    const [current_path, setCurrentPath] = useState(url_path);
    const [current_hashed_path, setCurrentHashedPath] = useState(hash_path(url_path));
    console.info(current_path);

    const navigate = (path: string) => {
        const hashed_path = path.replaceAll(param_regex, '\\VARIABLE\\')
        window.location.hash = path;
        setCurrentPath(path);
        setCurrentHashedPath(hashed_path)
    };

    let route_map = {};
    Children.map(props.children, child => {
        const path_hash = child.props.path.replaceAll(param_regex, '\\VARIABLE\\')
        route_map[path_hash] = child;
    });

    if (!Object.hasOwn(route_map, current_hashed_path)) {
        return <p>Page not found</p>;
    }

    const active_route = route_map[current_hashed_path];

    return (
        <navigator value={navigate}>
            { active_route }
        </navigator>
    );
}
