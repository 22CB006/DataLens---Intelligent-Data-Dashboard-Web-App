# DataLens Testing Guide

## 📋 Overview

This guide covers comprehensive testing for both backend and frontend of DataLens.

---

## 🔧 Backend Testing (Python/FastAPI)

### Setup

```bash
cd backend

# Install testing dependencies
pip install -r requirements-test.txt

# Or install individually
pip install pytest pytest-cov pytest-asyncio httpx faker
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test class
pytest tests/test_auth.py::TestUserRegistration

# Run specific test
pytest tests/test_auth.py::TestUserRegistration::test_register_new_user

# Run tests with markers
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m "not slow"    # Skip slow tests

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l

# Run tests in parallel (install pytest-xdist first)
pytest -n auto
```

### Test Structure

```
backend/tests/
├── conftest.py           # Shared fixtures and configuration
├── test_auth.py          # Authentication tests
├── test_datasets.py      # Dataset management tests
├── test_analysis.py      # Data analysis tests
└── test_services.py      # Service layer tests (to be added)
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser

# Check coverage percentage
pytest --cov=app --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=app --cov-fail-under=70
```

### Writing Tests

#### Example: Unit Test
```python
def test_password_hashing():
    """Test password hashing function."""
    password = "SecurePassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
```

#### Example: Integration Test
```python
@pytest.mark.integration
def test_complete_auth_flow(client):
    """Test complete authentication flow."""
    # Register
    register_response = client.post("/api/v1/auth/register", json={...})
    assert register_response.status_code == 201
    
    # Login
    login_response = client.post("/api/v1/auth/login", data={...})
    token = login_response.json()["access_token"]
    
    # Access protected endpoint
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
```

### Test Fixtures

Available fixtures in `conftest.py`:
- `db_session` - Fresh database session
- `client` - FastAPI test client
- `test_user` - Regular test user
- `test_superuser` - Admin test user
- `auth_token` - Authentication token
- `auth_headers` - Authorization headers
- `test_dataset` - Sample dataset
- `sample_csv_file` - Sample CSV file for upload

### Continuous Integration

```yaml
# .github/workflows/backend-tests.yml
name: Backend Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
```

---

## ⚛️ Frontend Testing (React/Vitest)

### Setup

```bash
cd frontend

# Install testing dependencies
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event @vitest/ui jsdom
```

### Update package.json

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:run": "vitest run"
  }
}
```

### Running Tests

```bash
# Run tests in watch mode
npm test

# Run tests once
npm run test:run

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run specific test file
npm test FileList.test.jsx

# Run tests matching pattern
npm test -- --grep "FileList"
```

### Test Structure

```
frontend/src/tests/
├── setup.js                      # Test setup and configuration
├── components/
│   ├── FileList.test.jsx        # FileList component tests
│   ├── ConfirmModal.test.jsx    # Modal component tests
│   └── Charts/
│       ├── BarChart.test.jsx
│       └── Heatmap.test.jsx
├── pages/
│   ├── Dashboard.test.jsx
│   ├── Analysis.test.jsx
│   └── Login.test.jsx
├── services/
│   ├── api.test.js
│   ├── authService.test.js
│   └── datasetService.test.js
└── hooks/
    └── useToast.test.js
```

### Writing Frontend Tests

#### Example: Component Test
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ConfirmModal from '../ConfirmModal';

describe('ConfirmModal', () => {
  it('renders when open', () => {
    render(
      <ConfirmModal
        isOpen={true}
        onClose={vi.fn()}
        onConfirm={vi.fn()}
        title="Test Modal"
        message="Test message"
      />
    );
    
    expect(screen.getByText('Test Modal')).toBeInTheDocument();
  });
  
  it('calls onConfirm when confirm button clicked', () => {
    const onConfirm = vi.fn();
    
    render(
      <ConfirmModal
        isOpen={true}
        onClose={vi.fn()}
        onConfirm={onConfirm}
      />
    );
    
    fireEvent.click(screen.getByText('Confirm'));
    expect(onConfirm).toHaveBeenCalled();
  });
});
```

#### Example: Service Test
```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import authService from '../authService';
import api from '../api';

vi.mock('../api');

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });
  
  it('login returns token on success', async () => {
    const mockResponse = {
      data: { access_token: 'test-token', token_type: 'bearer' }
    };
    api.post.mockResolvedValue(mockResponse);
    
    const result = await authService.login('test@example.com', 'password');
    
    expect(result.access_token).toBe('test-token');
    expect(api.post).toHaveBeenCalledWith('/auth/login', expect.any(Object));
  });
});
```

### Test Coverage

```bash
# Generate coverage report
npm run test:coverage

# View coverage report
# Open coverage/index.html in browser
```

### Mocking

#### Mock API Calls
```javascript
import { vi } from 'vitest';
import api from '../services/api';

vi.mock('../services/api');

// In test
api.get.mockResolvedValue({ data: mockData });
```

#### Mock React Router
```javascript
import { vi } from 'vitest';
import { useNavigate } from 'react-router-dom';

vi.mock('react-router-dom', () => ({
  ...vi.importActual('react-router-dom'),
  useNavigate: vi.fn(),
}));

// In test
const mockNavigate = vi.fn();
useNavigate.mockReturnValue(mockNavigate);
```

---

## 🎯 Test Coverage Goals

### Backend
- **Overall**: 70%+
- **Critical paths** (auth, data processing): 90%+
- **API endpoints**: 80%+
- **Service layer**: 75%+

### Frontend
- **Components**: 70%+
- **Services**: 80%+
- **Critical user flows**: 90%+

---

## 🚀 Best Practices

### General
1. **Write tests first** (TDD) when possible
2. **Test behavior, not implementation**
3. **Keep tests simple and focused**
4. **Use descriptive test names**
5. **Avoid test interdependencies**
6. **Mock external dependencies**
7. **Test edge cases and error conditions**

### Backend
1. Use fixtures for common setup
2. Test both success and failure cases
3. Verify HTTP status codes
4. Check response data structure
5. Test authentication and authorization
6. Validate input data
7. Test database transactions

### Frontend
1. Test user interactions
2. Verify component rendering
3. Test state changes
4. Mock API calls
5. Test error handling
6. Verify navigation
7. Test accessibility

---

## 📊 Test Reports

### Backend Coverage Report
```bash
cd backend
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

### Frontend Coverage Report
```bash
cd frontend
npm run test:coverage
# Open coverage/index.html
```

---

## 🐛 Debugging Tests

### Backend
```bash
# Run with pdb debugger
pytest --pdb

# Print output
pytest -s

# Verbose output with local variables
pytest -vl
```

### Frontend
```bash
# Run specific test with debug output
npm test -- --reporter=verbose FileList.test.jsx

# Use console.log in tests (will show in output)
console.log(screen.debug());
```

---

## 📝 Test Checklist

### Before Committing
- [ ] All tests pass
- [ ] Coverage meets minimum threshold
- [ ] No console errors or warnings
- [ ] Tests are properly named and organized
- [ ] Mocks are cleaned up after tests
- [ ] Test data is realistic
- [ ] Edge cases are covered
- [ ] Error handling is tested

### Before Deploying
- [ ] All integration tests pass
- [ ] Performance tests pass
- [ ] Security tests pass
- [ ] Cross-browser tests pass (frontend)
- [ ] API contract tests pass
- [ ] Database migration tests pass

---

## 🔗 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Best Practices](https://testingjavascript.com/)

---

## 🎉 Quick Start

### Backend
```bash
cd backend
pip install -r requirements-test.txt
pytest --cov=app
```

### Frontend
```bash
cd frontend
npm install
npm test
```

**Happy Testing! 🧪**
