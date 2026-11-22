<script>
    import { createEventDispatcher } from "svelte";
    import { apiCall } from "../lib/api";

    const dispatch = createEventDispatcher();
    let username = "";
    let password = "";
    let isRegistering = false;

    async function handleSubmit() {
        try {
            if (isRegistering) {
                await apiCall("/users/", "POST", {
                    username: username,
                    email: `${username}@test.com`,
                    password_plaintext: password,
                });
                alert("registered. logging you in");
                isRegistering = false;
                return handleSubmit();
            }

            const res = await apiCall("/auth/login", "POST", {
                username_or_email: username,
                password_plaintext: password,
            });
            localStorage.setItem("token", res.token);
            localStorage.setItem("user", JSON.stringify(res.user));
            localStorage.setItem("roles", JSON.stringify(res.roles));

            dispatch("login");
        } catch (e) {
            alert("uh oh:" + e.message);
        }
    }
</script>

<div class="login-box">
    <h2 id="login-header">{isRegistering ? "register" : "login"}</h2>

    <input type="text" bind:value={username} placeholder="username here" />
    <input type="password" bind:value={password} placeholder="password here" />

    <button on:click={handleSubmit}>
        {isRegistering ? "register" : "login"}
    </button>

    <p
        class="help-text"
        style="cursor:pointer;"
        on:click={() => (isRegistering = !isRegistering)}
    >
        {isRegistering
            ? "registered already? log in please."
            : "no account? click here to make a new one."}
    </p>
</div>

<style>
    .login-box h2 {
        text-align: left;
    }
    .help-text {
        font-size: 0.9rem;
        cursor: pointer;
    }
    input {
        color: var(--text, #ffffff);
    }
</style>
