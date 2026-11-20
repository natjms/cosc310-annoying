import { useEffect, useState } from 'react';

import { get_restaurant } from '@/client/restaurant'
import type { Restaurant } from '@/client/restaurant'
import { get_restaurant_menus } from '@/client/menu'
import type { Menu } from '@/client/menu'

import DisplayTable from '@/components/display-table'

type RestaurantPageProps = {
    restaurant_id: string;
};
export default function RestaurantPage({ restaurant_id }: RestaurantPageProps) {
    const [restaurant, setRestaurant]: [Restaurant, (r: Restaurant) => void] = useState(null);
    const [menus, setMenus]: [Menu[], (r: Menu[]) => void] = useState(null);
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

    if ((restaurant === null || menu === null) && error === null) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p> Error: {error} </p>;
    }

    return <>
        <h1> {restaurant.name} </h1>
        <DisplayTable item={restaurant} />

        <h2> Menus </h2>
        <ul>
            { menus.map(menu =>
                <li><a href={`/_/${restaurant_id}/${menu.id}`}>{menu.name}</a></li>
            )}
        </ul>
    </>
}
