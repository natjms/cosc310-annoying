import { useState } from 'react'
import { route } from 'preact-router'

type LogInPageProps = {
    created: boolean;
};
export default function LogInPage({ created }: LogInPageProps) {
    const [email, setEmail]: [string, (e: string) => void]  = useState('');
    const [password, setPassword]: [string, (e: string) => void] = useState('');

    const handleLogin = (e) => {
        e.preventDefault()

        // TODO: call the log in endpoint, set the session values

        route('/');
    }

    const inputHandler = (setter) => {
        return (e) => {
            setter(e.target.value)
        };
    };

    return <>
        <h1>Log in</h1>
        { created &&
            <p> Success! Your account has been created. You may now log in. </p>
        }
        <form action='#' onSubmit={handleLogin}>
            <input placeholder='email' type='email' value={email} onChange={inputHandler(setEmail)} required={true} /><br/>
            <input placeholder='Password' type='password' value={password} onChange={inputHandler(setPassword)} required={true} /><br/>
            <input value='Log in' type='submit' />
        </form>
    </>;
}
