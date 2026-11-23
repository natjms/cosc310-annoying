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
    params: object;
};

export function Route(props: RouteProps) {
    const {path, component, params} = props;
    component.props.params = params;
    return component;
}

const trim_trailing_slash = (path: string): string => {
    let trimmed = path;

    if (trimmed.length > 1 && trimmed.substring(trimmed.length - 1) == '/') {
        trimmed = trimmed.substring(0, trimmed.length - 1)
    }

    return trimmed;
};

const path_to_regex = (path: string): RegExp => {
    let trimmed_path = trim_trailing_slash(path);

    return new RegExp(
        `^${trimmed_path}$`.replaceAll('/', '\\/')
               .replaceAll(/{[A-Za-z_]\w*}/g, '(\\w*)'), 'g'
    );
};

const collect_path_params = (base_path: string, real_path: string): object => {
    let base = trim_trailing_slash(base_path).split('/');
    if (base[0] === '') {
        base = base.splice(1);
    }

    let real = trim_trailing_slash(real_path).split('/');
    if (real[0] === '') {
        real = real.splice(1);
    }

    let params = {};
    for (let i in base) {
        if (base[i][0] === '{' && base[i][base[i].length - 1] === '}') {
            const param_name = base[i].substring(1, base[i].length - 1);
            params[param_name] = real[i];
        }
    }

    return params;
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

    const navigate_controller = (path: string) => {
        window.location.hash = path;
        setCurrentPath(trim_trailing_slash(path));
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
    let non_route_components = [];
    Children.map(props.children, child => {
        if (child.type === Route) {
            route_map[child.props.path] = {
                path_regex: path_to_regex(child.props.path),
                component: child
            };
        } else {
            non_route_components.push(child);
        }
    });

    let active_route = null;
    for (let path in route_map) {
        // FIXME: This test will not pass, seemingly though it should, when the
        // user has refreshed the page and the current route is one with path
        // parameters.
        if (route_map[path].path_regex.test(current_path)) {
            active_route = route_map[path].component;
            active_route.props.params = collect_path_params(path, current_path);
            break;
        }
    }

    if (active_route === null) {
        return <p>Page not found</p>;
    }

    return (
        <NavigationContext value={navigate_controller}>
            { non_route_components }
            { active_route }
        </NavigationContext>
    );
}
