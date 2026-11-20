import { useState } from 'react'
import { route } from 'preact-router'
import Form from '@/components/form'

export default function CreateAccountPage() {
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = (form_data) => {
        // TODO: call the create user endpoint

        route('/login?created=true');
    }

    return (
        <Form
            name='Create account'
            callback={handleSubmit}
            error={error}
            fields={[
                {
                    label: 'Username',
                    type: 'text',
                    key: 'username',
                    required: true,
                },
                {
                    label: 'Email',
                    type: 'email',
                    key: 'email',
                    required: true,
                },
                {
                    label: 'Password',
                    type: 'password',
                    key: 'password_plaintext',
                    required: true,
                },

            ]}/>
    );
}
