---
name: fastapi-routes
description: "Create or modify FastAPI routes. Use when: adding new API endpoints, creating Pydantic request/response models, registering routers, designing REST APIs, or following route conventions for this project."
---

# FastAPI Routes

> **context7**: If the `context7_query-docs` tool is available, resolve and load the full `fastapi` documentation before proceeding:
> ```
> context7_resolve-library-id: "fastapi"
> context7_query-docs: /fastapi/fastapi "<your query>"
> ```

Guidelines and patterns for writing FastAPI routes in this codebase.

---

## REST Principles

APIs must adhere as closely as possible to REST principles, including appropriate use of HTTP verbs:

| Verb     | Usage                            |
| -------- | -------------------------------- |
| `GET`    | Read one or many resources       |
| `POST`   | Create a new resource            |
| `PUT`    | Replace / fully update a resource |
| `PATCH`  | Partial update (use sparingly)   |
| `DELETE` | Remove a resource                |

---

## Pydantic Models

- **Always** use Pydantic models for both input and output — never use plain `dict` or `Any`.
- **Never** reuse the same model for input and output. Use separate models:
  - `PostCreate` — user input for creating a resource
  - `PostUpdate` — user input for updating (optional fields)
  - `PostRead` — response shape returned to the client
- Parameters in **input** models must use `Field()` with validation constraints and a `description`.
- Output models do not require `Field()` unless you need aliases or serialization control.

```python
from uuid import UUID
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Post title")
    content: str = Field(min_length=1, description="Post content")


class PostRead(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: str


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200, description="Post title")
    content: str | None = Field(default=None, description="Post content")
```

---

## Router Pattern

Use `APIRouter` for all routes. Register the router in `{{cookiecutter.__package_slug}}/www.py`.

```python
from uuid import UUID

from fastapi import APIRouter, status

router = APIRouter()


@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate) -> PostRead:
    ...


@router.get("/posts/{post_id}", response_model=PostRead)
async def get_post(post_id: UUID) -> PostRead:
    ...


@router.put("/posts/{post_id}", response_model=PostRead)
async def update_post(post_id: UUID, post: PostUpdate) -> PostRead:
    ...


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: UUID) -> None:
    ...
```

---

## Route Registration

Register routers in `{{cookiecutter.__package_slug}}/www.py` using `app.include_router()`.

**Exceptions** (no prefix by convention):
- `/health` — liveness probe
- `/` — root redirect to docs
- `/static` — static file serving

---

## OpenAPI Docs

The OpenAPI documentation is served at these fixed paths — do not move them:

| URL               | Interface    |
| ----------------- | ------------ |
| `/docs`           | Swagger UI   |
| `/redoc`          | ReDoc        |
| `/openapi.json`   | Raw schema   |

---

## Error Handling

Use `HTTPException` with appropriate status codes:

```python
from fastapi import HTTPException, status

@router.get("/posts/{post_id}", response_model=PostRead)
async def get_post(post_id: UUID) -> PostRead:
    post = await get_post_from_db(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
```

---

## Dependency Injection

Use `Depends()` to inject shared logic (database sessions, authentication, etc.) into routes.

```python
from fastapi import Depends

from {{cookiecutter.__package_slug}} import get_db


@router.get("/posts/{post_id}", response_model=PostRead)
async def get_post(post_id: UUID, db = Depends(get_db)) -> PostRead:
    ...
```

---

## Lifespan

Use the `lifespan` parameter on the `FastAPI` app instance for startup and shutdown logic. Do not use the deprecated `@app.on_event("startup")` / `@app.on_event("shutdown")` decorators.

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await initialize_database()
    yield
    # Shutdown logic
    await close_database()


app = FastAPI(lifespan=lifespan)
```

---

## Style Checklist

Before submitting a new route, verify:

- [ ] HTTP verb matches the operation semantics
- [ ] Separate `Create`, `Update`, and `Read` models defined
- [ ] All input model fields use `Field()` with description
- [ ] Route is `async`
- [ ] Router is registered in `{{cookiecutter.__package_slug}}/www.py`
- [ ] 201 status used for `POST` create endpoints
- [ ] 204 status used for `DELETE` endpoints (no response body)
- [ ] Path parameters use typed UUIDs where appropriate

---

## Further Reading

- [docs/dev/api.md](../../docs/dev/api.md) — Full FastAPI developer guide covering the application structure, startup events, Swagger UI, ReDoc, OpenAPI schema, middleware, and dependency injection patterns.
- [FastAPI Docs](https://fastapi.tiangolo.com/)
