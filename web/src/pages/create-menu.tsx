import { useState } from 'react'
import { route } from 'preact-router'
import Form from '@/components/form'

type CreateMenuPageProps = {
    restaurant_id: string
};
export default function CreateMenuPage({ restaurant_id }) {
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = (form_data) => {
        // TODO: call the create endpoint
        route(`/_/${restaurant_id}/`);
    };

    return (
        <Form
            name='Create a new menu'
            callback={handleSubmit}
            error={error}
            fields={[
                {
                    label: 'Menu Name',
                    type: 'text',
                    key: 'name',
                    required: true,
                },
            ]}/>
    );
}
