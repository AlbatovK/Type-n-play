import requests
from requests import Response
from requests import adapters

base_server_url: str = None

adapter = adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)

session = requests.Session()
words_session = requests.Session()


def api_operation(func: callable) -> callable:
    def wrapper(url: str, params: dict) -> Response:
        return func(base_server_url + url, params) if base_server_url else None

    return wrapper


def init_api_service(base: str) -> None:
    global base_server_url
    base_server_url = base


@api_operation
def get_api_request(url: str, params: dict = None) -> Response:
    return session.get(url=url, params=params)


def create_session() -> int:
    return get_api_request(url="session/create", params=None).json()


def enter_session(session_id: int) -> int:
    params: dict = {"session_id": session_id}
    return get_api_request(url="session/enter", params=params).json()


def get_last_event(session_id: int) -> dict:
    params: dict = {"session_id": session_id}
    return get_api_request(url="session/event/last", params=params).json()


def post_event(session_id: int, event_code) -> None:
    params: dict = {"session_id": session_id, "event_code": event_code}
    get_api_request(url="session/event/post", params=params)
