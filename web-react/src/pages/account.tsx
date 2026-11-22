import { useEffect, useState } from 'react';

import { get_user } from '@/client/user'
import type { User } from '@/client/user'

import { useSecurity } from '@/utils/security'
import DisplayTable from '@/components/display-table'

export default function AccountPage() {
    const [user, setUser]: [User, (r: User) => void] = useState(null);
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const security = useSecurity();

    useEffect(() => {
        (async () => {
            const response = await get_user(security.user.id);

            if (!response.ok) {
                setError((await response.json()).detail);
                return;
            }

            setUser(await response.json());
        })();
    }, []);

    if (user === null) {
        return <p>Loading...</p>;
    }

    return <>
        <h1> {user.username} </h1>
        <DisplayTable item={user} />
        <a href='/account/update'>Update account</a>
    </>
}
