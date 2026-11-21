import { useState } from 'react'
import { route } from 'preact-router'
import { create_user } from '@/client/user'
import type { User } from '@/client/user'
import Form from '@/components/form'

export default function CreateAccountPage() {
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});

    const handleSubmit = async (form_data) => {
        const response = await create_user(form_data);

        if (response.status === 409) {
            throw 'A user with this username or email already exists. Please try another';
        }

        if (response.status === 422) {
            throw response;
        }

        if (response.ok) {
            route('/login?created=true');
        }
    }

    return (
        <Form
            name='Create account'
            callback={handleSubmit}
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
