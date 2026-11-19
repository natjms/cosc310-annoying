import { useEffect, useState } from 'react';

import { get_all_restaurants } from '@/client/restaurant'
import type { Restaurant } from '@/client/restaurant'

export default function RestaurantListPage() {
    const [restaurants, setRestaurants]: [Restaurant[], (a: Restaurant[]) => void] = useState([]);
    useEffect(() => {
        (async () => {
            setRestaurants(await (get_all_restaurants().then(r => r.json())));
        })();
    }, []);
    return (
        <h1>All restaurants</h1>
    );
}
