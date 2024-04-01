from bs4 import BeautifulSoup

about_driver_expected_record = """
    <report>
        <id>16</id>
        <position>16</position>
        <abbreviation>DRR</abbreviation>
        <driver>Daniel Ricciardo</driver>
        <team>RED BULL RACING TAG HEUER</team>
        <start>2018-05-24 12:14:12.054000</start>
        <end>2018-05-24 12:11:24.067000</end>
        <result>167987</result>
    </report>
    """

report_expected_records = [
    '<id>1</id>',
    '<position>1</position>',
    '<abbreviation>SVF</abbreviation>',
    '<driver>Sebastian Vettel</driver>',
    '<team>FERRARI</team>',
    '<start>2018-05-24 12:02:58.917000</start>',
    '<end>2018-05-24 12:04:03.332000</end>',
    '<result>64415</result>',
    '<id>2</id>',
    '<position>2</position>',
    '<abbreviation>VBM</abbreviation>',
    '<driver>Valtteri Bottas</driver>',
    '<team>MERCEDES</team>',
    '<start>2018-05-24 12:00:00</start>',
    '<end>2018-05-24 12:01:12.434000</end>',
    '<result>72434</result>',
]

drivers_expeted_records = [
    '<id>1</id>',
    '<abbreviation>SVF</abbreviation>',
    '<name>Sebastian Vettel</name>',
    '<team>FERRARI</team>',
    '<id>2</id>',
    '<abbreviation>VBM</abbreviation>',
    '<name>Valtteri Bottas</name>',
    '<team>MERCEDES</team>',
    '<id>3</id>',
    '<abbreviation>SVM</abbreviation>',
    '<name>Stoffel Vandoorne</name>',
    '<team>MCLAREN RENAULT</team>',
]


def test_report_xml(client):
    response = client.get('/api/v1/report/?format=xml')

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'xml')

    actual_records = [
        str(record)
        for record in soup.find_all(
            [
                'id',
                'position',
                'abbreviation',
                'driver',
                'team',
                'start',
                'end',
                'result',
            ]
        )[:16]
    ]

    assert actual_records == report_expected_records


def test_drivers_xml(client) -> None:
    response = client.get('/api/v1/report/drivers/?format=xml')

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'xml')

    actual_records = [
        str(record)
        for record in soup.find_all(
            [
                'id',
                'abbreviation',
                'name',
                'team',
            ]
        )[:12]
    ]
    assert actual_records == drivers_expeted_records


def test_about_driver_xml(client) -> None:
    url = '/api/v1/report/drivers/about/?abbr=DRR&format=xml'
    response = client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'xml')
    assert (
        soup.prettify()
        == BeautifulSoup(about_driver_expected_record, 'xml').prettify()
    )
