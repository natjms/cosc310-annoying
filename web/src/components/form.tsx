import { useState } from 'react'

type Field = {
    label: string;
    key
    type: string;
    required: boolean;
};

type FormProps = {
    name: string
    error: string
    fields: [];
    callback: (e) => void;
};

export default function Form(props: FormProps) {
    const {name, fields, callback, error, extra_message} = props;
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});

    const submitHandler = (e) => {
        e.preventDefault();
        callback(form_state);
    };

    const setter = (key) => {
        return e => {
            setFormState({...form_state, [key]: e.target.value});
        }
    };

    return <>
        <h1> {name} </h1>
        { error &&
            <p class='form:error-message'>{error}</p>
        }

        <form action='#' onSubmit={callback}>
            <table>
                <tbody>
                    { fields.map((field, i) =>
                        <tr key={i}>
                            <th>
                                <label for={`form-table-${i}`}>{field.label}</label>
                            </th>
                            <td>
                                <input
                                    id={`form-table-${i}`}
                                    type={field.type}
                                    value={form_state[field.key]}
                                    required={field.required}
                                    onChange={setter(field.key)}/>
                            </td>
                        </tr>
                    )}
                    <tr>
                        <td></td>
                        <td>
                            <input value='Submit' type='submit' />
                        </td>
                    </tr>
                </tbody>
            </table>
        </form>
    </>;
}
