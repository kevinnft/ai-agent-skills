---
name: api-testing
description: REST/GraphQL API testing with automated validation — test endpoints, validate responses, check status codes, and ensure API contracts
tags: [api, testing, rest, graphql, validation, automation]
origin: unknown
source_license: see upstream
language: en
---

# API Testing — Automated Endpoint Validation

Test REST and GraphQL APIs with automated validation. Verify endpoints, status codes, response schemas, performance, and security. Ensure API contracts are maintained across changes.

## When to Use

- Testing REST/GraphQL endpoints
- Validating API responses
- Contract testing between services
- Performance testing APIs
- Security testing endpoints
- CI/CD API validation

## Testing Approaches

### 1. Manual Testing (curl)
```bash
# GET request
curl -X GET https://api.example.com/users

# POST with JSON
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'

# With authentication
curl -X GET https://api.example.com/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Save response
curl -X GET https://api.example.com/users -o response.json

# Show headers
curl -i https://api.example.com/users

# Verbose output
curl -v https://api.example.com/users
```

### 2. Automated Testing (Python + requests + pytest)
```python
import requests
import pytest

BASE_URL = "https://api.example.com"

def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    
    # Status code
    assert response.status_code == 200
    
    # Response structure
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # First user structure
    user = data[0]
    assert "id" in user
    assert "name" in user
    assert "email" in user

def test_create_user():
    payload = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    
    response = requests.post(
        f"{BASE_URL}/users",
        json=payload
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data

def test_authentication_required():
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401

def test_invalid_data():
    payload = {"name": ""}  # Invalid: empty name
    response = requests.post(
        f"{BASE_URL}/users",
        json=payload
    )
    assert response.status_code == 400
    assert "error" in response.json()

def test_not_found():
    response = requests.get(f"{BASE_URL}/users/99999")
    assert response.status_code == 404
```

### 3. Schema Validation (jsonschema)
```python
import requests
from jsonschema import validate

user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "email"]
}

def test_user_schema():
    response = requests.get(f"{BASE_URL}/users/1")
    data = response.json()
    
    # Validate against schema
    validate(instance=data, schema=user_schema)
```

### 4. GraphQL Testing
```python
def test_graphql_query():
    query = """
    query {
        users {
            id
            name
            email
        }
    }
    """
    
    response = requests.post(
        f"{BASE_URL}/graphql",
        json={"query": query}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "users" in data["data"]
    assert len(data["data"]["users"]) > 0
```

## Testing Patterns

### 1. Setup/Teardown
```python
import pytest

@pytest.fixture
def test_user():
    """Create test user, cleanup after test"""
    # Setup
    response = requests.post(
        f"{BASE_URL}/users",
        json={"name": "Test User", "email": "test@example.com"}
    )
    user = response.json()
    
    yield user
    
    # Teardown
    requests.delete(f"{BASE_URL}/users/{user['id']}")

def test_with_fixtures(test_user):
    response = requests.get(f"{BASE_URL}/users/{test_user['id']}")
    assert response.status_code == 200
```

### 2. Parametrized Tests
```python
@pytest.mark.parametrize("endpoint,expected_status", [
    ("/users", 200),
    ("/posts", 200),
    ("/comments", 200),
    ("/invalid", 404),
])
def test_endpoints(endpoint, expected_status):
    response = requests.get(f"{BASE_URL}{endpoint}")
    assert response.status_code == expected_status
```

### 3. Performance Testing
```python
import time

def test_response_time():
    start = time.time()
    response = requests.get(f"{BASE_URL}/users")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 1.0  # Must respond within 1 second
```

### 4. Contract Testing
```python
def test_api_contract():
    """Ensure API contract hasn't changed"""
    response = requests.get(f"{BASE_URL}/users/1")
    user = response.json()
    
    # Required fields must exist
    required_fields = ["id", "name", "email", "created_at"]
    for field in required_fields:
        assert field in user, f"Missing required field: {field}"
    
    # Field types must match
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["email"], str)
```

## Best Practices

### 1. Test Error Cases
```python
def test_error_cases():
    # Invalid data
    response = requests.post(f"{BASE_URL}/users", json={})
    assert response.status_code == 400
    
    # Unauthorized
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401
    
    # Not found
    response = requests.get(f"{BASE_URL}/users/99999")
    assert response.status_code == 404
```

### 2. Test Pagination
```python
def test_pagination():
    response = requests.get(f"{BASE_URL}/users?page=1&limit=10")
    data = response.json()
    
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert len(data["items"]) <= 10
```

## Running Tests

```bash
# Run all tests
pytest tests/api/

# Run with coverage
pytest tests/api/ --cov

# Run specific test
pytest tests/api/test_users.py::test_get_users

# Run with verbose output
pytest tests/api/ -v
```

## References

- [pytest Documentation](https://docs.pytest.org/)
- [requests Documentation](https://requests.readthedocs.io/)
- [JSON Schema](https://json-schema.org/)
