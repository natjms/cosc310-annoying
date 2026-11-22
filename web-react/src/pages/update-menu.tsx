import { useState } from 'react'
import { route } from 'preact-router'
import Form from '@/components/form'

type UpdateMenuPageProps = {
    restaurant_id: string
    menu_id: string
};
export default function UpdateMenuPage({ restaurant_id, menu_id }: UpdateMenuPageProps) {
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = (form_data) => {
        // TODO: call the create endpoint
        route(`/_/${restaurant_id}/${menu_id}?updated=true`);
    };

    return (
        <Form
            name='Update menu'
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
