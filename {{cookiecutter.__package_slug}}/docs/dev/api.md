# FastAPI

This project uses [FastAPI](https://fastapi.tiangolo.com/), a modern, fast web framework for building APIs with Python based on standard Python type hints.

## Application Structure

The FastAPI application is defined in `{{cookiecutter.__package_slug}}/www.py` and includes:

- **Automatic API documentation** at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- **Static file serving** from `{{cookiecutter.__package_slug}}/static/` via the `/static/` endpoint
- **OpenAPI schema** available at `/openapi.json`
- **Root redirect** from `/` to `/docs` for convenient access to documentation

## Configuration

### Environment Variables

FastAPI-specific settings can be configured through environment variables in the Settings class:

- **PROJECT_NAME**: The name of the project (displayed in API docs)
- **DEBUG**: Enable debug mode (default: `False`)
  - Shows detailed error messages
  - Enables hot-reload in development

### Startup Events

The application automatically initializes required services on startup:
{%- if cookiecutter.include_aiocache == "y" %}

- **Cache initialization**: If aiocache is enabled, caches are configured and ready
{%- endif %}
{%- if cookiecutter.include_sqlalchemy == "y" %}

Note: Database connections are NOT initialized at startup. Instead, they are established lazily when first accessed via dependency injection (see Database Integration section below).
{%- endif %}

## Adding Routes

### Basic Route

Create a new route in `{{cookiecutter.__package_slug}}/www.py`:

```python
@app.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}
```

### Route with Path Parameters

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # FastAPI automatically validates user_id is an integer
    return {"user_id": user_id, "name": "John Doe"}
```

### Route with Query Parameters

```python
from typing import Optional

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10, search: Optional[str] = None):
    # Query params: ?skip=0&limit=10&search=foo
    return {"skip": skip, "limit": limit, "search": search}
```

### Route with Request Body

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

@app.post("/users")
async def create_user(user: UserCreate):
    # FastAPI automatically validates and deserializes the JSON body
    return {"user": user.dict(), "id": 123}
```

## Response Models

Use Pydantic models to define response schemas:

```python
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    # FastAPI ensures the response matches UserResponse schema
    return {
        "id": user_id,
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": datetime.now()
    }
```

## Dependency Injection

FastAPI's dependency injection system allows you to share logic across routes:

```python
from fastapi import Depends, HTTPException

async def get_current_user(token: str = Header(...)):
    # Validate token and get user
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"username": "johndoe"}

@app.get("/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user
```

{%- if cookiecutter.include_sqlalchemy == "y" %}

## Database Integration

If SQLAlchemy is enabled, use dependency injection for database sessions:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from {{cookiecutter.__package_slug}}.services.db import get_session_depends

@app.get("/users")
async def list_users(session: AsyncSession = Depends(get_session_depends)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users
```

{%- endif %}

## Error Handling

### Custom Exception Handlers

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

### Raising HTTP Exceptions

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Static Files

Static files are served from `{{cookiecutter.__package_slug}}/static/`:

1. **Add files** to the `static/` directory:

   ```
   {{cookiecutter.__package_slug}}/static/
   ├── css/
   │   └── styles.css
   ├── js/
   │   └── app.js
   └── images/
       └── logo.png
   ```

2. **Access files** via the `/static/` URL path:
   - `http://localhost:8000/static/css/styles.css`
   - `http://localhost:8000/static/images/logo.png`

## Middleware

Add middleware for cross-cutting concerns:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Background Tasks

Run tasks in the background without blocking the response:

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic here
    print(f"Sending email to {email}: {message}")

@app.post("/send-notification")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Hello from FastAPI!")
    return {"message": "Notification will be sent"}
```

## Testing

### Using the FastAPI Client Fixture

The project includes a `fastapi_client` fixture in `tests/conftest.py` that provides a TestClient instance. Use this fixture in your tests:

```python
# tests/conftest.py
import pytest_asyncio
from fastapi.testclient import TestClient
from {{cookiecutter.__package_slug}}.www import app


@pytest_asyncio.fixture
async def fastapi_client():
    """Fixture to create a FastAPI test client."""
    client = TestClient(app)
    yield client
```

### Writing Tests with the Fixture

Use the `fastapi_client` fixture in your test functions:

```python
# tests/test_www.py

def test_root_redirects_to_docs(fastapi_client):
    """Test that root path redirects to /docs."""
    response = fastapi_client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/docs"


def test_root_redirect_follows(fastapi_client):
    """Test that following redirect from root goes to docs."""
    response = fastapi_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    # Should reach the OpenAPI docs page


def test_api_endpoint(fastapi_client):
    """Test a custom API endpoint."""
    response = fastapi_client.get("/api/users/123")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 123
```

### Testing POST Requests

```python
def test_create_user(fastapi_client):
    """Test creating a user via POST."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    response = fastapi_client.post("/api/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
```

### Testing with Headers

```python
def test_authenticated_endpoint(fastapi_client):
    """Test endpoint that requires authentication."""
    headers = {"Authorization": "Bearer test-token"}
    response = fastapi_client.get("/api/me", headers=headers)
    assert response.status_code == 200
```

## Running the Application

### Development

```bash
# Using uvicorn directly
uvicorn {{cookiecutter.__package_slug}}.www:app --reload --host 0.0.0.0 --port 8000

# The app is accessible at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Production

```bash
# With more workers for production
uvicorn {{cookiecutter.__package_slug}}.www:app --host 0.0.0.0 --port 8000 --workers 4

# Or using gunicorn with uvicorn workers
gunicorn {{cookiecutter.__package_slug}}.www:app -w 4 -k uvicorn.workers.UvicornWorker
```

{%- if cookiecutter.include_docker == "y" %}

### Docker

If Docker is configured, use docker-compose:

```bash
docker-compose up www
```

{%- endif %}

## Best Practices

1. **Use Response Models**: Always define Pydantic models for responses to ensure type safety and automatic documentation

2. **Leverage Dependency Injection**: Use `Depends()` to share logic like authentication, database sessions, and configuration

3. **Async All the Way**: Use `async def` for route handlers when performing I/O operations (database, external APIs, file operations)

4. **Validate Input**: Leverage Pydantic's validation for request bodies and FastAPI's parameter validation for path and query parameters

5. **Document Your API**: Add docstrings to route functions - they appear in the auto-generated docs:

   ```python
   @app.get("/users")
   async def list_users():
       """
       Retrieve a list of all users.

       Returns a paginated list of user objects with their basic information.
       """
       return users
   ```

6. **Use HTTP Status Codes**: Return appropriate status codes (201 for created, 204 for no content, etc.):

   ```python
   from fastapi import status

   @app.post("/users", status_code=status.HTTP_201_CREATED)
   async def create_user(user: UserCreate):
       return {"user": user}
   ```

7. **Separate Concerns**: Keep business logic separate from route handlers - use service layers or utility modules

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
