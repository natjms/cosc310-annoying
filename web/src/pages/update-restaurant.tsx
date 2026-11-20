import { useState } from 'react'
import { route } from 'preact-router'
import Form from '@/components/form'

export default function UpdateRestaurantPage() {
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = (form_data) => {
        // TODO: call the create user endpoint

        route('/restaurant?created=true');
    };

    return (
        <Form
            name='Update a restaurant'
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
