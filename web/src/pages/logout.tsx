import { useState } from 'react'
import { Redirect } from '@/utils/nats-friendly-router'
import * as security from '@/utils/security'

export default function LogOutPage() {
    const [should_log_out, setShouldLogOut]: [boolean, (s: boolean) => void] = useState(false);

    const handleLogout = () => {
        localStorage.setItem(security.LOCALSTORAGE_LOGOUT_FLAG, 'true');
        setShouldLogOut(true);
    };

    if (should_log_out) {
        return <Redirect to='/' />;
    }

    return <>
        <h1> Log out </h1>

        <p>Are you sure you want to log out?</p>
        <button onClick={handleLogout}>
            Yes, log out now
        </button>
    </>;
}
