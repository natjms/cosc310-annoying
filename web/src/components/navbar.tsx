import { Link } from '@/utils/nats-friendly-router'
import { useSecurity } from '@/utils/security'

import '@/components/navbar.css'

export default function Navbar() {
    const security = useSecurity();

    return <nav class='navbar:container'>
        <ul>
            <li><Link path='/'>Home</Link></li>
            <li><Link path='/restaurants'>Restaurants</Link></li>

            { security === null ?
                <li><Link path='/login'>Log in</Link></li>
                : <li><Link path='/logout'>Log out</Link></li>
            }
        </ul>
    </nav>
}
