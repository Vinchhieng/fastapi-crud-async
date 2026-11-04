import pytest

from app.api import events_crud

PAYLOAD = {
    "title": "Mekong Jazz Night",
    "city": "Phnom Penh",
    "price_usd": 15.0,
    "seats_left": 320,
}
EVENT = {"id": 1, **PAYLOAD}


@pytest.fixture
def event_store(monkeypatch):
    """Fresh data per test, with async CRUD replacements like the notes tests."""
    store = {1: EVENT.copy()}

    async def post(payload):
        event_id = max(store, default=0) + 1
        store[event_id] = {"id": event_id, **payload.dict()}
        return event_id

    async def get(id):
        return store.get(id)

    async def get_all():
        return list(store.values())

    async def put(id, payload):
        store[id] = {"id": id, **payload.dict()}
        return id

    async def delete(id):
        del store[id]
        return id

    for name, replacement in [("post", post), ("get", get), ("get_all", get_all),
                              ("put", put), ("delete", delete)]:
        monkeypatch.setattr(events_crud, name, replacement)
    return store


def test_create_event(test_app, event_store):
    response = test_app.post("/events/", json=PAYLOAD)
    assert response.status_code == 201
    assert response.json() == {"id": 2, **PAYLOAD}
    assert event_store[2] == response.json()


def test_read_event(test_app, event_store):
    response = test_app.get("/events/1/")
    assert response.status_code == 200
    assert response.json() == EVENT


def test_read_all_events(test_app, event_store):
    response = test_app.get("/events/")
    assert response.status_code == 200
    assert response.json() == [EVENT]


def test_missing_event(test_app, event_store):
    response = test_app.get("/events/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_update_event(test_app, event_store):
    payload = {**PAYLOAD, "title": "Updated Jazz Night", "seats_left": 0}
    response = test_app.put("/events/1/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **payload}
    assert test_app.get("/events/1/").json() == response.json()


@pytest.mark.parametrize("field,value", [
    ("title", "ab"), ("title", "a" * 81),
    ("city", "a"), ("city", "a" * 51),
    ("price_usd", -1), ("seats_left", -1),
])
@pytest.mark.parametrize("method,path", [("POST", "/events/"), ("PUT", "/events/1/")])
def test_invalid_event_data(test_app, event_store, field, value, method, path):
    response = test_app.request(method, path, json={**PAYLOAD, field: value})
    assert response.status_code == 422
    assert any(error["loc"][-1] == field for error in response.json()["detail"])
    assert event_store == {1: EVENT}


@pytest.mark.parametrize("field", list(PAYLOAD))
def test_missing_required_field(test_app, event_store, field):
    payload = {key: value for key, value in PAYLOAD.items() if key != field}
    response = test_app.post("/events/", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
def test_zero_id_is_422(test_app, event_store, method):
    response = test_app.request(method, "/events/0/", json=PAYLOAD if method == "PUT" else None)
    assert response.status_code == 422
    assert event_store == {1: EVENT}


@pytest.mark.parametrize("method", ["PUT", "DELETE"])
def test_missing_event_mutation(test_app, event_store, method):
    response = test_app.request(method, "/events/999/", json=PAYLOAD if method == "PUT" else None)
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_delete_event(test_app, event_store):
    response = test_app.delete("/events/1/")
    assert response.status_code == 200
    assert response.json() == EVENT
    assert test_app.get("/events/1/").status_code == 404
    assert event_store == {}


def test_zero_prices_and_seats_are_valid(test_app, event_store):
    payload = {**PAYLOAD, "price_usd": 0, "seats_left": 0}
    response = test_app.post("/events/", json=payload)
    assert response.status_code == 201
    assert response.json()["price_usd"] == 0
    assert response.json()["seats_left"] == 0

