from deployer.config_utils import (
    get_nginx_config,
    get_systemd_config,
    get_uwsgi_config
)


def test_get_nginx_config():
    result = get_nginx_config(
        'test_app', ['test_app.com', 'www.test_app.com'], 'python')

    assert result

    assert 'test_app' in result
    assert 'test_app.com' in result


def test_get_systemd_config():
    result = get_systemd_config('test_app')

    assert result

    assert 'test_app' in result


def test_get_uwsgi_config():
    result = get_uwsgi_config('test_app')

    assert result

    assert 'test_app' in result
