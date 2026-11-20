import { useState } from 'react'
import { route } from 'preact-router'
import Form from '@/components/form'

type LogInPageProps = {
    created: boolean;
};
export default function LogInPage({ created }: LogInPageProps) {
    const [error, setError]: [object, (o: object) => void] = useState(null);

    const handleLogin = (form_data) => {
        // TODO: call the log in endpoint, set the session values
        route('/');
    }

    return <>
        { created &&
            <p>Success! You can now log in</p>
        }
        <Form
            name='Log in'
            error={error}
            callback={handleLogin}
            fields={[
                {
                    label: 'Email',
                    type: 'email',
                    key: 'username_or_email',
                    required: true,
                },
                {
                    label: 'Password',
                    type: 'password',
                    key: 'password_plaintext',
                    required: true,
                },

            ]}/>
    </>;
}
