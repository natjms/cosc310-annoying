<script>
    import { onMount, createEventDispatcher } from "svelte";
    import { apiCall } from "../lib/api";

    const dispatch = createEventDispatcher();
    let restaurants = [];
    let error = "";
    let searchQuery = "";
    let expandedRestaurantId = null;
    let loadingMenu = false;
    let menusCache = {};
    let itemsCache = {};

    $: loadRestaurants(searchQuery);

    async function loadRestaurants(query = "") {
        try {
            if (query && query.trim() !== "") {
                restaurants = await apiCall(
                    `/restaurants/search?query=${encodeURIComponent(query)}`,
                );
            } else {
                restaurants = await apiCall("/restaurants/");
            }
            error = "";
        } catch (e) {
            error = e.message;
        }
    }

    async function toggleRestaurant(restaurantId) {
        if (expandedRestaurantId == restaurantId) {
            expandedRestaurantId = null;
            return;
        }

        expandedRestaurantId = restaurantId;

        if (!menusCache[restaurantId]) {
            loadingMenu = true;
            try {
                const menus = await apiCall(
                    `/menus/?restaurant=${restaurantId}`,
                );

                if (menus && menus.length > 0) {
                    const menu = menus[0];
                    menusCache[restaurantId] = menu;
                    const items = await apiCall(`/menu-items/?menu=${menu.id}`);
                    itemsCache[restaurantId] = items;
                } else {
                    menusCache[restaurantId] = null;
                }
            } catch (e) {
                console.error(":C menu didn't load", e);
            } finally {
                loadingMenu = false;
            }
        }
    }

    async function addToCart(restaurantId, menuItemId) {
        try {
            await apiCall(
                `/carts/${restaurantId}?menu_item_id=${menuItemId}&quantity=1`,
                "PATCH",
            );

            const btn = document.getElementById(`btn-${menuItemId}`);
            if (btn) {
                btn.innerText = "added";
                setTimeout(() => (btn.innerText = "+ Add"), 1000);
            }
        } catch (e) {
            alert(":C adding to cart failed" + e.message);
        }
    }
</script>

<h2>restaurants</h2>
{#if error}<p>ERROR!!!!!</p>{/if}

<input
    type="text"
    bind:value={searchQuery}
    placeholder="search for your favourite restaurant"
/>

<div class="restaurant-list">
    {#each restaurants as restaurant}
        <div class="restaurant-card">
            <div
                class="restaurant-header"
                on:click={() => toggleRestaurant(restaurant.id)}
            >
                <h3>{restaurant.name}</h3>
                <span class="expand-icon">
                    {expandedRestaurantId === restaurant.id ? "^" : "v"}
                </span>
            </div>

            {#if expandedRestaurantId === restaurant.id}
                <div class="restaurant-body">
                    {#if loadingMenu}
                        <p>loading....</p>
                    {:else if !menusCache[restaurant.id]}
                        <p>no menu available.</p>
                    {:else if itemsCache[restaurant.id] && itemsCache[restaurant.id].length > 0}
                        {#each itemsCache[restaurant.id] as item}
                            <div class="menu-item-row">
                                <span>
                                    {item.name} - ${item.price.toFixed(2)}
                                </span>
                                <button
                                    id="btn-{item.id}"
                                    class="btn-add"
                                    on:click|stopPropagation={() =>
                                        addToCart(restaurant.id, item.id)}
                                >
                                    + Add
                                </button>
                            </div>
                        {/each}
                        <button
                            class="primary"
                            style="width:100%; margin-top:1rem;"
                            on:click|stopPropagation={() =>
                                dispatch("select", restaurant.id)}
                        >
                            go to cart/checkout
                        </button>
                    {:else}
                        <p>no items added to the menu yet...</p>
                    {/if}
                </div>
            {/if}
        </div>
    {/each}
</div>
