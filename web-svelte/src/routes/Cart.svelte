<script>
    import { onMount, createEventDispatcher } from "svelte";
    import { apiCall } from "../lib/api";

    let restaurantName = "";
    export let restaurantId = null;
    const dispatch = createEventDispatcher();

    let cartsToDisplay = [];
    let error = "";
    let loading = true;

    async function resolveCartItems(cart) {
        let itemsWithDetails = [];
        let total = 0;

        for (const item of Object.values(cart.items)) {
            try {
                const menuItem = await apiCall(
                    `/menu-items/${item.menu_item_id}?menu=${item.menu_id}`,
                );
                itemsWithDetails.push({
                    ...item,
                    name: menuItem.name,
                    price: menuItem.price,
                    subtotal: menuItem.price * item.quantity,
                });
                total += menuItem.price * item.quantity;
            } catch (e) {
                console.error("uh oh couldnt fetch item details", e);
                itemsWithDetails.push({
                    ...item,
                    name: "unknown item",
                    price: 0,
                    subtotal: 0,
                });
            }
        }
        return { ...cart, resolvedItems: itemsWithDetails, totalPrice: total };
    }

    async function loadCarts() {
        loading = true;
        error = "";
        restaurantName = "";
        try {
            if (restaurantId) {
                const cart = await apiCall(`/carts/${restaurantId}`);

                if (Object.keys(cart.items).length > 0) {
                    const resolved = await resolveCartItems(cart);
                    resolved.restaurantId = restaurantId;
                    cartsToDisplay = [resolved];
                } else {
                    cartsToDisplay = [];
                }
            } else {
                const restaurants = await apiCall("/restaurants/");
                let allCarts = [];
                for (const r of restaurants) {
                    try {
                        const cart = await apiCall(`/carts/${r.id}`);
                        if (Object.keys(cart.items).length > 0) {
                            const resolved = await resolveCartItems(cart);
                            resolved.restaurantName = r.name;
                            resolved.restaurantId = r.id;
                            allCarts.push(resolved);
                        }
                    } catch (e) {}
                }
                cartsToDisplay = allCarts;
            }
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    }

    $: if (restaurantId !== undefined) {
        loadCarts();
    }

    async function checkout(cartId) {
        try {
            const cartToCheckout = cartsToDisplay.find((c) => c.id === cartId);
            await apiCall(
                `/orders/?restaurant_id=${cartToCheckout.restaurantId}`,
                "POST",
            );
            alert("order placed successfully!");
            cartsToDisplay = cartsToDisplay.filter((c) => c.id !== cartId);
            if (cartsToDisplay.length === 0) {
                dispatch("checkout");
            }
        } catch (e) {
            alert("uh oh checkout failed  " + e.message);
        }
    }

    async function removeItem(restaurantId, itemId) {
        try {
            await apiCall(`/carts/${restaurantId}/items/${itemId}`, "DELETE");
            await loadCarts();
        } catch (e) {
            alert("uh oh removing items failed: " + e.message);
        }
    }
</script>

<h2>
    {#if restaurantName}
        your cart at {restaurantName}
    {:else}
        your carts
    {/if}
</h2>
{#if loading}
    <p>loading.... time keeps marching forwards...</p>
{:else if error}
    <p>{error}</p>
{:else if cartsToDisplay.length === 0}<p>feeling hungry yet?</p>
    <!-- {:else if cart && Object.keys(cart.items).length > 0} -->
{:else}
    {#each cartsToDisplay as cart}
        <div class="restaurant-card">
            {#if cart.restaurantName}
                <h3>{cart.restaurantName}</h3>
            {:else}
                <h3>cart items</h3>
            {/if}
            <ul>
                {#each cart.resolvedItems as item}
                    <li>
                        <span>item id: {item.name} (x{item.quantity})</span>
                        <span>${item.subtotal.toFixed(2)}</span>
                        <button
                            on:click={() =>
                                removeItem(
                                    cart.restaurantId,
                                    item.menu_item_id,
                                )}
                        >
                            remove item
                        </button>
                    </li>
                {/each}
            </ul>
            <div>
                <p>total: ${cart.totalPrice.toFixed(2)}</p>
                <button
                    class="primary"
                    style="width:100%; margin-top:1rem;"
                    on:click={() => checkout(cart.id)}
                >
                    checkout the above cart?
                </button>
            </div>
        </div>
    {/each}
{/if}
