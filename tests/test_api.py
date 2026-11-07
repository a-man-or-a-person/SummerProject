def test_ping_endpoint(client):
    assert client.get('/ping').json() == {'Ping': 'ok'}

def test_invalid_inputs_and_unknown_links(client):
    assert client.post('/get_short', json={'url': 'not_a_url'}).status_code == 422
    assert client.get('/red/unknown', follow_redirects=False).status_code == 404
