from http import HTTPStatus
from pytest import fixture

from .utils import headers


def routes():
    yield '/respond/observables'
    yield '/respond/trigger'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


def test_respond_call_success(route, client, valid_jwt):
    response = client.post(route, headers=headers(valid_jwt()))
    assert response.status_code == HTTPStatus.OK
