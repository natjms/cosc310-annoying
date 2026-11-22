<script>
    import { onMount } from "svelte";
    import { apiCall } from "../lib/api";

    let orders = [];
    let error = "";
    let loading = true;

    async function resolveOrderItems(order) {
        let itemsWithDetails = [];

        for (const item of Object.values(order.items)) {
            try {
                const menuItem = await apiCall(
                    `/menu-items/${item.menu_item_id}?menu=${item.menu_id}`,
                );
                itemsWithDetails.push({
                    ...item,
                    name: menuItem.name,
                    subtotal: item.price_at_order_time * item.quantity,
                });
            } catch (e) {
                itemsWithDetails.push({
                    ...item,
                    name: "unknown item",
                    subtotal: 0,
                });
            }
        }
        return { ...order, resolvedItems: itemsWithDetails };
    }

    onMount(async () => {
        try {
            const rawOrders = await apiCall("/orders/");
            let resolvedOrders = [];

            for (const order of rawOrders) {
                resolvedOrders.push(await resolveOrderItems(order));
            }
            orders = resolvedOrders;
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    });
</script>

<h2>order history</h2>
{#if loading}<p>loading orders...</p>
{:else if error}<p>{error}</p>
{:else if orders.length === 0}
    <p>go order something first :p</p>
{:else}
    {#each orders as order}
        <div class="restaurant-card">
            <p>order id: {order.id}</p>
            <p>status: {order.status}</p>
            <p>total: {order.total_price.toFixed(2)}</p>
            <ul>
                {#each order.resolvedItems as item}
                    <li>
                        {item.name} (x{item.quantity}) - ${item.subtotal.toFixed(
                            2,
                        )}
                    </li>
                {/each}
            </ul>
        </div>
    {/each}
{/if}
