import { useState } from 'react'
import { route } from 'preact-router'

import { useSecurity } from '@/utils/security'
import { update_user } from '@/client/user'
import type { User } from '@/client/user'

import Form from '@/components/form'

export default function CreateAccountPage() {
    const security = useSecurity();
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = async (form_data) => {
        const response = await update_user(security.user.id, form_data);

        if (response.status === 409) throw 'Username or email already in use';
        if (response.status === 422) throw response;

        route('/account?updated=true');
    }

    return (
        <Form
            name='Update your account'
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
