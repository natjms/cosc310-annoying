import { route } from 'preact-router'
import * as security from '@/utils/security'

export default function LogOutPage() {

    const handleLogout = () => {
        localStorage.setItem(security.LOCALSTORAGE_LOGOUT_FLAG, 'true');
        route('/');
    };

    return <>
        <h1> Log out </h1>

        <p>Are you sure you want to log out?</p>
        <button onClick={handleLogout}>
            Yes, log out now
        </button>
    </>;
}
