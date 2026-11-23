import { useSecurity } from '@/utils/security'

import '@/components/navbar.css'

export default function Navbar() {
    const security = useSecurity();

    return <nav class='navbar:container'>
        <ul>
            <li><a href='/'>Home</a></li>
            <li><a href='/restaurants'>Restaurants</a></li>

            { security === null ?
                <>
                    <li><a href='/create-account'>Create account</a></li>
                    <li><a href='/login'>Log in</a></li>
                </>
                : <>
                    <li><a href='/account'>Account</a></li>
                    <li><a href='/logout'>Log out</a></li>
                </>
            }
        </ul>
    </nav>
}
