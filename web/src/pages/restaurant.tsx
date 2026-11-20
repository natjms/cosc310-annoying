import { useEffect, useState } from 'react';

import { get_restaurant } from '@/client/restaurant'
import type { Restaurant } from '@/client/restaurant'

import DisplayTable from '@/components/display-table'

type RestaurantPageProps = {
    restaurant_id: string;
};
export default function RestaurantPage({ restaurant_id }: RestaurantPageProps) {
    const [restaurant, setRestaurant]: [Restaurant, (r: Restaurant) => void] = useState(null);
    const [error, setError]: [string, (e: string) => void] = useState(null);

    useEffect(() => {
        (async () => {
            const response = await get_restaurant(restaurant_id);

            if (!response.ok) {
                setError((await response.json()).detail);
                return;
            }

            setRestaurant(await response.json());
        })();
    }, []);

    if (restaurant === null) {
        return <p>Loading...</p>;
    }

    return <>
        <h1> {restaurant.name} </h1>
        <DisplayTable item={restaurant} />
    </>
}
