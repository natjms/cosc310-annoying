<script>
    import Cart from "./routes/Cart.svelte";
    import Orders from "./routes/Orders.svelte";
    import Restaurants from "./routes/Restaurants.svelte";
    import Login from "./routes/Login.svelte";
    import Admin from "./routes/Admin.svelte";

    let currentPage = localStorage.getItem("token") ? "restaurants" : "login";
    let activeRestaurantId = null;

    function navigate(page, id = null) {
        if (id) activeRestaurantId = id;
        currentPage = page;
    }

    function logout() {
        localStorage.removeItem("token");
        navigate("login");
    }
</script>

<!-- html here -->
<nav>
    {#if currentPage !== "login"}
        <button on:click={() => navigate("restaurants")}>Restaurants</button>
        <button on:click={() => navigate("orders")}>My Orders</button>
        <button on:click={() => navigate("cart")}>My Cart</button>
        <button on:click={() => navigate("admin")}>Admin</button>
        <button style="color: #ff5555" on:click={logout}>Logout</button>
    {/if}
</nav>

<main>
    <h1 id="top-banner">annoying frontend</h1>
    <p id="password-hint">psst! the password is AVeryStr0ngPassw0rd!</p>
    <p id="separator">---------------------------------------------------</p>
    {#if currentPage === "login"}
        <Login on:login={() => navigate("restaurants")} />
    {:else if currentPage === "restaurants"}
        <Restaurants on:select={(e) => navigate("cart", e.detail)} />
    {:else if currentPage === "cart"}
        <Cart
            bind:restaurantId={activeRestaurantId}
            on:checkout={() => navigate("orders")}
        />
    {:else if currentPage === "orders"}
        <Orders />
    {:else if currentPage === "admin"}
        <Admin />
    {/if}
</main>

<!-- css below -->
<style>
    #top-banner {
        padding-bottom: 0rem;
        text-align: center;
    }
    #separator {
        text-align: center;
        font-weight: 100;
        padding-bottom: 2rem;
    }
    #password-hint {
        text-align: center;
        font-size: 0.8rem;
    }
</style>
