import { useState } from 'react'

import { Redirect } from '@/utils/nats-friendly-router'

export default function LogInPage() {
    const [email, setEmail]: [string, (e: string) => void]  = useState('');
    const [password, setPassword]: [string, (e: string) => void] = useState('');
    const [should_redirect, setShouldRedirect]: [boolean, (e: boolean) => void] = useState(false);

    const handleLogin = (e) => {
        e.preventDefault()

        // TODO: call the log in endpoint, set the session values

        setShouldRedirect(true);
    }

    if (should_redirect) {
        return <Redirect to='/' />
    }

    return <>
        <h1>Log in</h1>
        <form action='#' onSubmit={handleLogin}>
            <input placeholder='email' type='email' value={email} required={true} /><br/>
            <input placeholder='Password' type='password' value={password} required={true} /><br/>
            <input value='Log in' type='submit' />
        </form>
    </>;
}
