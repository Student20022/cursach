report_json = [
    {
        'abbreviation': 'SVF',
        'driver': 'Sebastian Vettel',
        'end': 'Thu, 24 May 2018 12:04:03 GMT',
        'id': 1,
        'position': 1,
        'result': 64415,
        'start': 'Thu, 24 May 2018 12:02:58 GMT',
        'team': 'FERRARI',
    },
    {
        'abbreviation': 'VBM',
        'driver': 'Valtteri Bottas',
        'end': 'Thu, 24 May 2018 12:01:12 GMT',
        'id': 2,
        'position': 2,
        'result': 72434,
        'start': 'Thu, 24 May 2018 12:00:00 GMT',
        'team': 'MERCEDES',
    },
    {
        'abbreviation': 'SVM',
        'driver': 'Stoffel Vandoorne',
        'end': 'Thu, 24 May 2018 12:19:50 GMT',
        'id': 3,
        'position': 3,
        'result': 72463,
        'start': 'Thu, 24 May 2018 12:18:37 GMT',
        'team': 'MCLAREN RENAULT',
    },
]

drivers_json = [
    {
        'abbreviation': 'SVF',
        'id': 1,
        'name': 'Sebastian Vettel',
        'team': 'FERRARI',
    },
    {
        'abbreviation': 'VBM',
        'id': 2,
        'name': 'Valtteri Bottas',
        'team': 'MERCEDES',
    },
    {
        'abbreviation': 'SVM',
        'id': 3,
        'name': 'Stoffel Vandoorne',
        'team': 'MCLAREN RENAULT',
    },
]


def test_report_json(client) -> None:
    response = client.get('/api/v1/report/?format=json')
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 19
    assert all('abbreviation' in entry for entry in data)

    for entry in report_json:
        for key, value in entry.items():
            assert (value in info for info in data)


def test_drivers_json(client) -> None:
    response = client.get('/api/v1/report/drivers/?format=json')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 19
    assert all('abbreviation' in entry for entry in data)

    for entry in drivers_json:
        for key, value in entry.items():
            assert (value in info for info in data)


def test_about_driver_json(client) -> None:
    response = client.get(
        '/api/v1/report/drivers/about/?abbr=DRR&format=json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert all('position' in entry for entry in data)

    for entry in report_json[2]:
        assert entry in data[0]
