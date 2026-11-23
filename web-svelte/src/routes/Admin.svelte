<script>
    import { onMount } from "svelte";
    import { apiCall } from "../lib/api";

    let user = {};
    let roles = [];
    let restaurants = [];
    let message = "";

    let expandedRestaurantId = null;
    let menusCache = {};

    onMount(() => {
        user = JSON.parse(localStorage.getItem("user") || "{}");
        roles = JSON.parse(localStorage.getItem("roles") || "[]");

        if (roles.includes("restaurateur")) {
            loadRestaurants();
        }
    });

    async function loadRestaurants() {
        try {
            const allRestaurants = await apiCall("/restaurants/");
            if (roles.includes("admin")) {
                restaurants = allRestaurants;
            } else if (roles.includes("restaurateur")) {
                restaurants = allRestaurants.filter(
                    (r) => r.owner_id === user.id,
                );
            } else {
                restaurants = [];
            }
        } catch (e) {
            message = "uh oh " + e.message;
        }
        restaurants = await apiCall("/restaurants/");
    }

    async function createRestaurant() {
        const name = prompt("restaurant name:");
        if (!name) return;
        try {
            await apiCall("/restaurants/", "POST", {
                name: name,
                owner_id: user.id,
            });
            message = "restaurant created";
            loadRestaurants();
        } catch (e) {
            message = "uh oh" + e.message;
        }
    }

    async function deleteRestaurant(restaurantId) {
        if (!confirm("delete this restaurant? ALL data will be gone.")) return;
        try {
            await apiCall(`/restaurants/${restaurantId}`, "DELETE");
            message = "restaurant deleted!";
            loadRestaurants();
        } catch (e) {
            message = "uh oh" + e.message;
        }
    }

    async function toggleRestaurant(restaurantId) {
        if (expandedRestaurantId === restaurantId) {
            expandedRestaurantId = null;
            return;
        }
        expandedRestaurantId = restaurantId;
        if (!menusCache[restaurantId]) {
            try {
                const menus = await apiCall(
                    `/menus/?restaurant=${restaurantId}`,
                );
                menusCache[restaurantId] = menus || [];
            } catch (e) {
                message = "uh oh" + e.message;
            }
        }
    }

    async function createMenu(restaurantId) {
        const name = prompt("menu name? ");
        if (!name) return;
        try {
            await apiCall(`/menus`, "POST", {
                restaurant_id: restaurantId,
                name: name,
            });
            message = "menu created.";
            const menus = await apiCall(`/menus/?restaurant=${restaurantId}`);
            menusCache[restaurantId] = menus || [];
        } catch (e) {
            alert("uh oh  :" + e.message);
        }
    }

    async function deleteMenu(menuId, restaurantId) {
        if (!confirm("delete this menu? ALL data will be gone.")) return;
        try {
            await apiCall(`/menus/${menuId}`, "DELETE");
            message = "menu deleted.";
            const menus = await apiCall(`/menus/?restaurant=${restaurantId}`);
            menusCache[restaurantId] = menus || [];
        } catch (e) {
            alert("uh oh  :" + e.message);
        }
    }

    async function addMenuItem(menuId, restaurantId) {
        const name = prompt("Item name:");
        const price = prompt("Item price:");
        if (!name || !price) return;

        try {
            await apiCall(`/menu-items/?menu=${menuId}`, "POST", {
                name: name,
                price: parseFloat(price),
            });
            message = "item added.";
            const menus = await apiCall(`/menus/?restaurant=${restaurantId}`);
            menusCache[restaurantId] = menus || [];
        } catch (e) {
            alert("uh oh  :" + e.message);
        }
    }
    async function deleteMenuItem(menuId, itemId, restaurantId) {
        if (!confirm("delete this item?")) return;
        try {
            await apiCall(`/menu-items/${itemId}?menu=${menuId}`, "DELETE");
            message = "item deleted.";
            const menus = await apiCall(`/menus/?restaurant=${restaurantId}`);
            menusCache[restaurantId] = menus || [];
        } catch (e) {
            alert("uh oh... :" + e.message);
        }
    }
</script>

<h2>admin panel</h2>
<p>welcome, {user.username}.</p>

{#if roles.includes("admin")}
    <p>global admins can do anything</p>
{:else if roles.includes("restaurateur")}
    <p>restaurant manager can manage their own restaurants</p>
{:else}<p>you are a customer. focus on the food instead?</p>
{/if}

{#if roles.includes("restaurateur") || roles.includes("admin")}
    <div class="management-section">
        <h3>your restaurants</h3>
        {#each restaurants as r}
            <div class="card">
                <p>{r.name}</p>
                <button
                    on:click={() =>
                        alert("todo: manage menu page is not added yet")}
                >
                    manage menu?
                </button>
            </div>
        {/each}

        <h3>create new restaurant?</h3>
        <input type="text" placeholder="restaurant name" />
        <button class="primary" on:click={createRestaurant}>
            create restaurant
        </button>
    </div>
{/if}
{#if message}<p>{message}</p>{/if}
