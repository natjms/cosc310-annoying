import { useContext, createContext, useState, useEffect, Children } from 'react';

const NavigationContext = createContext(null);
export const useNavigation = () => useContext(NavigationContext);


type LinkProps = {
    children: ReactNode;
    path: string;
};
export function Link(props: LinkProps) {
    const navigate = useNavigation();

    return <a href={`#${props.path}`} onClick={() => navigate(props.path)}>{props.children}</a>;
}

type RedirectProps = {
    to: string
};

export function Redirect(props: RedirectProps) {
    const navigate = useNavigation();
    navigate(props.to);
}

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

    const navigate_controller = (path: string) => {
        const hashed_path = path.replaceAll(param_regex, '\\VARIABLE\\')
        window.location.hash = path;
        setCurrentPath(path);
        setCurrentHashedPath(hashed_path)
    };

    // By handling the popstate event we can ensure that the browser's back
    // button still works
    const history_change_controller = () => {
        navigate_controller(window.location.hash.substring(1));
    };
    window.addEventListener('popstate', history_change_controller);
    useEffect(() => {
        return () => {
            // Remove the listener when the component is unmounted
            window.removeEventListener('popstate', history_change_controller);
        }
    });

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
        <NavigationContext value={navigate_controller}>
            { active_route }
        </NavigationContext>
    );
}
