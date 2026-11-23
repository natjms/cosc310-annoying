import * as requests from '@/client/requests'
export function get_restaurant_menus(restaurant_id) : Promise<Response> {
    return requests.get(`/menus/?restaurant=${restaurant_id}`);
}

export function create_menu(restaurant_id, name) {
    return requests.post('/menus/', {body: {restaurant_id, name}});
}

export function get_menu_items(menu_id) {
    return requests.get('/menu-items', {query: {menu: menu_id}});
}

export function create_menu_item(payload, menu_id) {
    return requests.post('/menu-items/', {body: payload, query: {menu: menu_id}});
}
