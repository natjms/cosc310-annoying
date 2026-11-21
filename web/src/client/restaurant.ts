import * as requests from '@/client/requests'

export type RestaurantAddress = {
    name: string;
    street: string;
    unit: string;
    city: string;
    province: string;
    zip_code: string;
};

export type Restaurant = {
    id: string;
    owner_id: string;
    name: string
    description: string;
    address: RestaurantAddress;
    phone_number: string;
    is_active: boolean;
};

export function get_all_restaurants() : Promise<Response> {
    return requests.get('/restaurants/');
}

export function get_restaurant(id: string) : Promise<Response> {
    return requests.get(`/restaurants/${id}`);
}

export function create_restaurant(owner_id, name) {
    return requests.post('/restaurants/', {body: {
        owner_id, name
    }});
}
