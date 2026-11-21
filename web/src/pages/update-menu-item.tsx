import { useState } from 'react'
import { route } from 'preact-router'
import Form from '@/components/form'

type UpdateMenuItemPageProps = {
    restaurant_id: string
    menu_id: string
    menu_item_id: string
};
export default function UpdateMenuItemPage({ restaurant_id, menu_id, menu_item_id }: UpdateMenuItemPageProps) {
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = (form_data) => {
        // TODO: call the create endpoint
        route(`/_/${restaurant_id}/${menu_id}/${menu_item}?updated=true`);
    };

    return (
        <Form
            name='Update a menu item'
            callback={handleSubmit}
            error={error}
            fields={[
                {
                    label: 'Name',
                    type: 'text',
                    key: 'name',
                    required: true,
                },
                {
                    label: 'Price',
                    type: 'number',
                    key: 'price',
                    required: true,
                },
            ]}/>
    );
}
