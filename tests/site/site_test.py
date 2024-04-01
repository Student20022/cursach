def test_index_redirect(client) -> None:
    response = client.get('/')
    assert response.status_code == 302
    assert '/report' in response.location


def test_report_page_asc_order(client) -> None:
    response = client.get('/report?order=asc')
    assert response.status_code == 200
    assert 'text/plain; charset=utf-8' in response.content_type
    assert 'position' in response.get_data(as_text=True)
    assert len(response.get_data(as_text=True).split('\n')) == 20
    assert (
        response.get_data(as_text=True).split('\n')[1]
        == '|    1 |          1 | SVF           ' + 
        ' | Sebastian Vettel  | FERRARI                   | ' + 
        '2018-05-24 12:02:58.917000 | 2018-05-24 12:04:03.332000 |    64415 |'
    )


def test_report_page_desc_order(client) -> None:
    response = client.get('/report?order=desc')
    assert response.status_code == 200
    assert 'text/plain; charset=utf-8' in response.content_type
    assert 'position' in response.get_data(as_text=True)
    assert len(response.get_data(as_text=True).split('\n')) == 20
    assert (
        response.get_data(as_text=True).split('\n')[1]
        == '|   19 |         19 | LHM            ' +
        '| Lewis Hamilton    | MERCEDES                  | '
        '2018-05-24 12:18:20.125000 | 2018-05-24 12:11:32.585000 |   407540 |' 
    )


def test_driver_list_asc(client) -> None:
    response = client.get('/report/drivers/?order=asc')
    html_content = response.data.decode('utf-8')
    assert response.status_code == 200
    assert 'text/html' in response.content_type
    assert 'Abbreviation' in html_content
    assert html_content.count('<tr>') == 20


def test_driver_list_desc(client) -> None:
    response = client.get('/report/drivers/?order=desc')
    html_content = response.data.decode('utf-8')
    assert response.status_code == 200
    assert 'text/html' in response.content_type
    assert 'Abbreviation' in html_content
    assert html_content.count('<tr>') == 20


def test_about_driver(client) -> None:
    response = client.get('/report/drivers?abbr=SVF')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data == [
        {
            'abbreviation': 'SVF',
            'driver': 'Sebastian Vettel',
            'end': 'Thu, 24 May 2018 12:04:03 GMT',
            'id': 1,
            'position': 1,
            'result': 64415,
            'start': 'Thu, 24 May 2018 12:02:58 GMT',
            'team': 'FERRARI',
        }
    ]
