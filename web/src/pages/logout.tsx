import { route } from 'preact-router'
import { log_out } from '@/client/auth'
import * as security from '@/utils/security'

export default function LogOutPage() {

    const handleLogout = async () => {
        const _ = await log_out();

        localStorage.removeItem(security.LOCALSTORAGE_USER_KEY);
        localStorage.removeItem(security.LOCALSTORAGE_ROLE_KEY);
        localStorage.removeItem(security.LOCALSTORAGE_TOKEN_KEY);

        window.location.href = '/';
    };

    return <>
        <h1> Log out </h1>

        <p>Are you sure you want to log out?</p>
        <button onClick={handleLogout}>
            Yes, log out now
        </button>
    </>;
}
