import { useEffect, useState } from 'react';

import { get_menu, get_menu_items } from '@/client/menu'
import type { Menu, MenuItem } from '@/client/menu'

import DisplayTable from '@/components/display-table'

type MenuPageProps = {
    restaurant_id: string;
    menu_id: string;
};
export default function MenuPage({ restaurant_id, menu_id }: MenuPageProps) {
    const [menu, setMenu]: [Menu, (r: Menu) => void] = useState(null);
    const [menu_items, setMenuItems]: [MenuItem[], (r: MenuItem[]) => void] = useState(null);
    const [error, setError]: [string, (e: string) => void] = useState(null);

    useEffect(() => {
        (async () => {
            const response = await get_menu(menu_id);

            if (!response.ok) {
                setError((await response.json()).detail);
                return;
            }

            setMenu(await response.json());
        })();
    }, []);

    if ((menu === null || menu_items === null) && error === null) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p> Error: {error} </p>;
    }

    return <>
        <h1> {menu.name} </h1>
        <DisplayTable item={menu} />

        <h2> Menus Items </h2>
        <ul>
            { menu_items.map(item =>
                <li><a href={`/_/${restaurant_id}/${menu_id}/${item.id}`}>{item.name}, {item.price}</a></li>
            )}
        </ul>
    </>
}
