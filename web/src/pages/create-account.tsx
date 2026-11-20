import { useState } from 'react'
import { route } from 'preact-router'

export default function CreateAccountPage() {
    const [username, setUsername]: [string, (e: string) => void]  = useState('');
    const [email, setEmail]: [string, (e: string) => void]  = useState('');
    const [password, setPassword]: [string, (e: string) => void] = useState('');
    const [error, setError]: [string, (e: string) => void] = useState(null);
    

    const handleLogin = (e) => {
        e.preventDefault()

        // TODO: call the create user endpoint

        route('/login?created=true');
    }

    const inputHandler = (setter) => {
        return (e) => {
            setter(e.target.value)
        };
    };

    return <>
        <h1>Create account</h1>
        { error !== null &&
            <p> { error } </p>
        }
        <form action='#' onSubmit={handleLogin}>
            <input placeholder='username' type='text' value={username} onChange={inputHandler(setUsername)} required={true} /><br/>
            <input placeholder='email' type='email' value={email} onChange={inputHandler(setEmail)} required={true} /><br/>
            <input placeholder='Password' type='password' value={password} onChange={inputHandler(setPassword)} required={true} /><br/>
            <input value='Log in' type='submit' />
        </form>
    </>;
}
