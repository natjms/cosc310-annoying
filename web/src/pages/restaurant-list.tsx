import { useEffect, useState } from 'react'

import { route } from 'preact-router'
import { get_all_restaurants } from '@/client/restaurant'
import type { Restaurant } from '@/client/restaurant'

type RestaurantListPageProps = {
    query: string
};
export default function RestaurantListPage({ query }: RestaurantListPageProps) {
    const [restaurants, setRestaurants]: [Restaurant[], (a: Restaurant[]) => void] = useState(null);
    const [search_query, setSearchQuery]: [string, (s: string) => void] = useState(query);
    const [should_search, setShouldSearch]: [boolean, (b: boolean) => void] = useState(false);
    const [error, setError]: [string, (e: string) => void] = useState(null);

    useEffect(() => {
        (async () => {
            const response = await get_all_restaurants();

            if (!response.ok) {
                setError((await response.json()).detail);
            } else {
                setRestaurants(await response.json())
            }
        })();
    }, []);

    const search_query_change_handler = (e) => setSearchQuery(e.target.value);
    const search_handler = () => {
        setShouldSearch(true);
    };

    if (should_search) {
        route(`/restaurants?query=${search_query}`);
    }

    if (restaurants === null) {
        return <p>Loading...</p>
    }

    return <>
        <h1>All restaurants</h1>

        <input placeholder='Search restaurants' value={search_query} onChange={search_query_change_handler} />
        <button onClick={search_handler}>
            Search
        </button>

        { restaurants.length === 0 ?
            <p>No restaurants found!</p>
            : <ul>
                { restaurants.map(restaurant =>
                    <li><a href={`/_/${restaurant.id}/`}>{restaurant.name}</a></li>
                )}
            </ul>
        }
    </>;
}
