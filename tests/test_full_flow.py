def test_full_url_flow_and_duplicate_request(client):
    first = client.post('/get_short', json={'url': 'https://example.com/path'})
    again = client.post('/get_short', json={'url': 'https://example.com/path'})
    assert first.status_code == again.status_code == 201
    assert first.json() == again.json()
    assert first.json()['short_url'].startswith('http://testserver/red/')
    response = client.get(first.json()['short_url'], follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['location'] == 'https://example.com/path'
