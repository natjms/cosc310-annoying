import { useState } from 'react'
import { route } from 'preact-router'
import { create_menu_item } from '@/client/menu'
import Form from '@/components/form'

type CreateMenuPageProps = {
    restaurant_id: string
    menu_id: string
};
export default function CreateMenuItemPage({ restaurant_id, menu_id }) {
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);

    const handleSubmit = async (form_data) => {
        // TODO: call the create endpoint
        const response = await create_menu_item(form_data, menu_id);
        if (!response.ok) throw response;
        //route(`/_/${restaurant_id}/`);
    };

    return (
        <Form
            name='Create a new menu item'
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
