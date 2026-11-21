import { useState } from 'react'
import { route } from 'preact-router'

import { useSecurity } from '@/utils/security'
import { create_restaurant } from '@/client/restaurant'
import Form from '@/components/form'

export default function CreateRestaurantPage() {
    const security = useSecurity();
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = async (form_data) => {
        const response = await create_restaurant(security.user.id, form_data.name);
        route('/restaurant?created=true');
    };

    return (
        <Form
            name='Create a new restaurant'
            callback={handleSubmit}
            error={error}
            fields={[
                {
                    label: 'Restaurant Name',
                    type: 'text',
                    key: 'name',
                    required: true,
                },
            ]}/>
    );
}
