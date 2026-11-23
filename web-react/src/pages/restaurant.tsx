import { useEffect, useState } from 'react';

import { get_restaurant } from '@/client/restaurant'
import type { Restaurant } from '@/client/restaurant'
import { get_restaurant_menus, get_menu_items } from '@/client/menu'
import { useSecurity } from '@/utils/security'

import DisplayTable from '@/components/display-table'

type RestaurantPageProps = {
    restaurant_id: string;
};
export default function RestaurantPage({ restaurant_id }: RestaurantPageProps) {
    const security = useSecurity();
    const [restaurant, setRestaurant]: [Restaurant, (r: Restaurant) => void] = useState(null);
    const [menus, setMenus]: [Menu[], (r: Menu[]) => void] = useState(true);
    const [menu_items, setMenuItems] = useState(null);
    const [error, setError]: [string, (e: string) => void] = useState(null);

    useEffect(() => {
        (async () => {
            const restaurant_response = await get_restaurant(restaurant_id);
            const menu_response = await get_restaurant_menus(restaurant_id);

            if (!restaurant_response.ok) {
                setError((await response.json()).detail);
                return;
            }

            const retrieved_menus = await menu_response.json();
            let items = {};

            for (let menu of retrieved_menus) {
                const response = await get_menu_items(menu.id);
                items[menu.id] = await response.json();
            }

            setRestaurant(await restaurant_response.json());
            setMenus(retrieved_menus);
            setMenuItems(items);
        })();
    }, []);

    if ((restaurant === null || menus === null || menu_items === null) && error === null) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p> Error: {error} </p>;
    }

    return <>
        <h1> {restaurant.name} </h1>
        <DisplayTable item={restaurant} />

        <h2> Menus </h2>

        { security && security.role.includes('restaurateur') &&
            <p>
                <a href={`/_/${restaurant_id}/create-menu`}>Create a new restaurant</a>
            </p>
        }

        
        <ul>
            { menus.map(menu =>
                <li>
                    <a href={`/_/${restaurant_id}/${menu.id}`}>{menu.name}</a> - 

                    { security && security.role.includes('restaurateur') &&
                    <a href={`/_/${restaurant_id}/${menu.id}/create-menu-item`}>Add</a>
                    }

                    { menu_items[menu.id] > 0 &&
                        <ol>
                            {menu_items[menu.id].map(item =>
                                <li>{item.name} - {item.price}</li>
                            )}
                        </ol>
                    }
                </li>
            )}
        </ul>
    </>
}
