import { useState } from 'react'
import { route } from 'preact-router'
import { log_in } from '@/client/auth'
import * as security from '@/utils/security'
import Form from '@/components/form'

type LogInPageProps = {
    created: boolean;
};
export default function LogInPage({ created }: LogInPageProps) {
    const handleLogin = async (form_data) => {
        const response = await log_in(form_data);

        if (response.status === 401) throw 'Your credentials are incorrect. Please try again';
        if (response.status === 422) throw response;

        const { user, roles, token } = await response.json();

        localStorage.setItem(security.LOCALSTORAGE_USER_KEY, JSON.stringify(user));
        localStorage.setItem(security.LOCALSTORAGE_TOKEN_KEY, token);
        localStorage.setItem(security.LOCALSTORAGE_ROLE_KEY, JSON.stringify(roles));

        window.location.href = '/';
    }

    return <>
        { created &&
            <p>Success! You can now log in</p>
        }
        <Form
            name='Log in'
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
