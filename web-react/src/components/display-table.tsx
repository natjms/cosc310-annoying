type DisplayTableProps = {
    item: object;
};

export default function DisplayTable(props: DisplayTableProps) {
    const { item } = props;

    let rows = [];
    for (let key of Object.keys(item).sort()) {
        let value = item[key];

        if (key[0] == '_') {
            continue;
        }

        if (typeof value === 'object') {
            value = JSON.stringify(value);
        }

        rows.push([key, value]);
    }

    return <table>
        <tbody>
            { rows.map(row =>
                <tr>
                    <th>{row[0]}</th>
                    <td>{row[1]}</td>
                </tr>
            )}
        </tbody>
    </table>;
}
