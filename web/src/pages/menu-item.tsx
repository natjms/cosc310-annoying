import { useEffect, useState } from 'react';

import { get_menu, get_menu_items } from '@/client/menu'
import type { Menu, MenuItem } from '@/client/menu'

import DisplayTable from '@/components/display-table'

type MenuItemPageProps = {
    restaurant_id: string;
    menu_id: string;
    menu_item_id: string;
};
export default function MenuItemPage({ restaurant_id, menu_id, menu_item_id }: MenuPageProps) {
    const [menu_item, setMenuItem]: [MenuItem, (r: MenuItem) => void] = useState(null);
    const [error, setError]: [string, (e: string) => void] = useState(null);

    useEffect(() => {
        (async () => {
            const response = await get_menu_item(menu_item_id);

            if (!response.ok) {
                setError((await response.json()).detail);
                return;
            }

            setMenuItem(await response.json());
        })();
    }, []);

    const add_to_cart_handler = (e) => {};

    if (menu_items === null && error === null) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p> Error: {error} </p>;
    }

    return <>
        <h1> {menu_item.name} </h1>
        <DisplayTable item={menu_item} />

        <button onClick={add_to_cart_handler}>
            Add to cart
        </button>
    </>
}
