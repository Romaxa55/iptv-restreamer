import requests


def test_server_running():
    resp = requests.get('http://127.0.0.1:8000/status')
    assert resp.status_code == 200
    data = resp.json()
    expected_data = {'status': 'ok'}
    assert data == expected_data

def test_valid_url_index_m3u8():
    resp = requests.get('http://127.0.0.1:8000/iptv/xxxxxxxxxxx/1111/index.m3u8')
    assert resp.status_code == 200
def test_404():
    resp = requests.get('http://127.0.0.1:8000/iptv/1111/index.m3u8')
    assert resp.status_code == 404


