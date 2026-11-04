# Developing and Testing an Asynchronous API with FastAPI and Pytest

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/fastapi-crud).

## Want to use this project?

Build the images and run the containers:

```sh
$ docker-compose up -d --build
```

Test out the following routes:

1. [http://localhost:8002/ping](http://localhost:8002/ping)
1. [http://localhost:8002/docs](http://localhost:8002/docs)
1. [http://localhost:8002/notes](http://localhost:8002/notes)


## Events resource

The events resource follows the notes resource's async CRUD pattern and uses the
same PostgreSQL database. Event fields are `title` (3-80 characters), `city`
(2-50 characters), `price_usd` (nonnegative number), and `seats_left`
(nonnegative integer).

| Method | Path | Success |
| --- | --- | --- |
| POST | `/events/` | 201 |
| GET | `/events/` | 200 |
| GET | `/events/{id}/` | 200 |
| PUT | `/events/{id}/` | 200 |
| DELETE | `/events/{id}/` | 200 |

Missing events return `404` with `{"detail": "Event not found"}`. IDs must
be greater than zero; invalid IDs and payload fields return `422`.

### Run and verify

Start Docker Desktop and wait until its engine is running. From the project root:

```sh
docker compose up -d --build
docker compose exec web pytest .
```

Open http://localhost:8002/ping and http://localhost:8002/docs. The docs should
show five notes operations and five events operations, plus ping. Use the docs
to create, read, update, and delete an event against PostgreSQL.

The events tests follow the original notes tests by mocking the async database
functions. They cover create, single/list reads, missing IDs, update, deletion,
invalid fields, required fields, ID zero, and valid zero price/seats. Each events
test gets fresh data through a function-scoped fixture.

### Submission

Upload the changed and new source files to your fork, preserving their paths:

- `src/app/db.py`
- `src/app/main.py`
- `src/app/api/models.py`
- `src/app/api/events.py`
- `src/app/api/events_crud.py`
- `src/tests/test_events.py`

Include this README and `.gitignore` if publishing the whole project. Do not
upload `.venv`, caches, or local database files. Submit your fork URL in a text
file only after the Docker checks above pass.


### Dependency compatibility

AnyIO is pinned to 3.7.1 because the starter's Starlette 0.21.0 TestClient uses
`anyio.start_blocking_portal`, which AnyIO 4 removed. The original notes source
and tests are unchanged.
