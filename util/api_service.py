import requests

base_url: str = None


def api_operation(f):
    def wrapper(url: str, params):
        return f(base_url + url, params) if base_url else None

    return wrapper


def init_api_service(base: str):
    global base_url
    base_url = base


@api_operation
def get_api_request(url, params=None):
    req = requests.get(url, params=params)
    return req.json()


def create_session() -> int:
    return get_api_request(url="session/create", params=None)


def enter_session(session_id: int):
    params = {"session_id": session_id}
    get_api_request(url="session/enter", params=params)


def get_last_event(session_id: int):
    params = {"session_id": session_id}
    return get_api_request(url="session/event/last", params=params)


def post_event(session_id: int, event_code):
    params = {"session_id": session_id, "event_code": event_code}
    return get_api_request(url="session/event/post", params=params)


def get_random_words(count: int):
    params = {'number': count}
    return ' '.join(requests.get(url='https://random-word-api.herokuapp.com/word', params=params).json())
