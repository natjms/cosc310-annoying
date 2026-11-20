import { useState } from 'react'
import { route } from 'preact-router'

export default function LogInPage() {
    const [email, setEmail]: [string, (e: string) => void]  = useState('');
    const [password, setPassword]: [string, (e: string) => void] = useState('');

    const handleLogin = (e) => {
        e.preventDefault()

        // TODO: call the log in endpoint, set the session values

        route('/');
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
