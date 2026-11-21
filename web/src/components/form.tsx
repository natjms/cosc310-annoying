import { useState } from 'react'

type Field = {
    label: string;
    key
    type: string;
    required: boolean;
};

type FormProps = {
    name: string;
    fields: [];
    callback: (e) => void;
};

export default function Form(props: FormProps) {
    const {name, fields, callback} = props;
    const [form_state, setFormState]: [object, (o: object) => void] = useState({});
    const [error, setError]: [string, (e: string) => void] = useState(null);
    const [validation_errors, setValidationErrors]: [array, (v: array) => void] = useState(null);

    const submitHandler = async (e) => {
        e.preventDefault();
        setError(null);
        setValidationErrors(null);

        try {
            await callback(form_state);
        } catch (e) {
            if (typeof e === 'string') {
                setError(e);
            }

            if (e.status !== undefined) {
                if (e.status === 422) {
                    setValidationErrors((await e.json()).detail);
                }
            }
        }
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

        { validation_errors &&
            validation_errors.map(e =>
                <p>{e.msg.replaceAll('Value error, ', '')}</p>
            )
        }

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
                        <button onClick={submitHandler}>
                            Submit
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </>;
}
