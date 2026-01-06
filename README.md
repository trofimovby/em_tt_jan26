# Enterprise Order Management System

[![Project Status](https://img.shields.io/badge/status-completed-success?style=for-the-badge)](https://github.com)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django 5.0](https://img.shields.io/badge/django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF 3.14](https://img.shields.io/badge/DRF-3.14-red?style=for-the-badge)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)

A production-ready order management system featuring robust **Role-Based Access Control (RBAC)**, **JWT authentication**, and **automated API documentation**. Built with modern security best practices and enterprise-grade architecture.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project demonstrates a **comprehensive full-stack implementation** of a secure API service with emphasis on architecture excellence and security-first design principles. Unlike typical solutions, the system implements a **custom access control mechanism** that operates on top of JWT tokens through dedicated middleware and permission classes.

### Core Principles

- **Security First**: Custom JWT middleware with signature validation
- **Architectural Clarity**: Layered security approach with separation of concerns
- **Production Ready**: Comprehensive testing, documentation, and error handling
- **Developer Experience**: Interactive API documentation and intuitive client interface

---

## Key Features

### 🔐 Authentication & Authorization

- **Custom JWT Implementation**: Implemented from scratch without external JWT libraries, giving full control over token lifecycle and validation logic
- **Bearer Token Validation**: Middleware-based token extraction and verification with signature validation
- **Role-Based Access Control (RBAC)**: Flexible permission system allowing fine-grained control over CRUD operations per role and resource

### 📃 API & Documentation

- **OpenAPI/Swagger Documentation**: Auto-generated, interactive API documentation with drf-spectacular
- **RESTful API Design**: Clean, intuitive endpoints following REST conventions
- **Request/Response Examples**: Built-in examples in Swagger UI for all endpoints

### 🖥️ Frontend Client

- **Dashboard Interface**: Modern, responsive web dashboard built with HTML5, CSS3, and vanilla JavaScript
- **Asynchronous Operations**: Fetch API-based client with smooth user experience
- **Bootstrap 5 Integration**: Professional styling with Bootstrap framework
- **Real-time Updates**: Instant feedback on operations and state changes

### 🧪 Testing & Quality Assurance

- **Comprehensive Unit Tests**: Full coverage of user workflows (registration → login → order management)
- **Integration Testing**: End-to-end test scenarios for complete application workflows
- **Test Database**: Isolated test database to ensure test independence

---

## Technology Stack

### Backend

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Programming language |
| Django | 5.0+ | Web framework |
| Django REST Framework | 3.14+ | REST API toolkit |
| PyJWT | Latest | JWT token handling |
| Bcrypt | Latest | Password hashing |

### Frontend

| Technology | Purpose |
|-----------|---------|
| HTML5 | Markup structure |
| CSS3 | Styling and layout |
| JavaScript (ES6+) | Client-side logic |
| Bootstrap 5 | UI framework |
| Fetch API | HTTP requests |

### Database & Deployment

| Component | Purpose |
|-----------|---------|
| SQLite | Default database (easily replaceable with PostgreSQL) |
| Django ORM | Database abstraction layer |

---

## Architecture

The system implements a **multi-layered security architecture**:

### Layer 1: Middleware Authentication

The JWT middleware intercepts incoming requests and:
- Extracts the `Bearer` token from the `Authorization` header
- Validates the JWT signature using the secret key
- Decodes the token payload and extracts user information
- Injects the authenticated user object into the request context
- Returns 401 Unauthorized for invalid or missing tokens

### Layer 2: DRF Authentication Adapter

A custom authentication class that bridges the custom middleware with Django REST Framework's authentication system:
- Ensures compatibility with DRF's authentication expectations
- Allows seamless integration with ViewSets and APIViews
- Provides consistent authentication across all endpoints

### Layer 3: Permission System (RBAC)

The `RBACPermission` class implements granular access control:
- Queries the database for role-resource-method permissions
- Evaluates permissions based on user's assigned role
- Supports CRUD operations: CREATE, READ, UPDATE, DELETE
- Returns 403 Forbidden for unauthorized access attempts

### Data Flow

```
HTTP Request
    ↓
JWT Middleware (Validate Token)
    ↓
DRF Authentication Adapter
    ↓
RBACPermission Class (Check Permissions)
    ↓
ViewSet/APIView Handler
    ↓
HTTP Response
```

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Step 1: Clone and Setup Virtual Environment

```bash
git clone https://github.com/yourusername/em_tt_jan26.git
cd em_tt_jan26

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Migration and Initialization

```bash
# Apply database migrations
python manage.py migrate

# Seed database with initial roles, resources, and test user
python manage.py seed_db
```

The seed script will create:
- User roles: `admin`, `user`
- Resources: `orders` and related permissions
- Default admin account: `admin@example.com` / `admin123`

### Step 4: Run Development Server

```bash
python manage.py runserver
```

The server will be available at `http://127.0.0.1:8000`

---

## Quick Start

### Option 1: Web Dashboard

1. Open `index.html` in your web browser (double-click the file)
2. Login with default credentials:
   - **Email**: `admin@example.com`
   - **Password**: `admin123`
3. Access the order management dashboard to create and view orders

### Option 2: Swagger API Documentation

1. Navigate to `http://127.0.0.1:8000/api/docs/`
2. Click the "Authorize" button in the top-right corner
3. Authenticate using the `/api/auth/login/` endpoint:
   - **Email**: `admin@example.com`
   - **Password**: `admin123`
4. Copy the received token and paste it as `Bearer <token>` in the Authorize dialog
5. Test API endpoints directly in the browser with live examples

### Option 3: cURL/REST Client

```bash
# Get authentication token
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# Use token to access protected endpoints
curl -X GET http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer <your_token>"
```

---

## API Documentation

The API documentation is automatically generated and accessible via Swagger UI. Key endpoints:

### Authentication Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/login/` | Authenticate and receive JWT token |
| POST | `/api/auth/register/` | Create new user account |
| POST | `/api/auth/logout/` | Invalidate current session |

### Order Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/orders/` | List all accessible orders |
| POST | `/api/orders/` | Create a new order |
| GET | `/api/orders/{id}/` | Retrieve specific order |
| PATCH | `/api/orders/{id}/` | Update existing order |
| DELETE | `/api/orders/{id}/` | Delete an order |

> Full API specification available at `/api/docs/` with interactive examples.

---

## Testing

### Running Tests

Execute the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test module
python manage.py test core.tests.AuthenticationTests

# Run with coverage report
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage

The test suite includes:

- **Authentication Tests**: User registration, login, token validation
- **Authorization Tests**: Permission checking for different roles
- **Integration Tests**: Complete user workflows
- **Edge Cases**: Invalid tokens, expired sessions, malformed requests

---

## Project Structure

```
em_tt_jan26/
│
├── config/                          # Django configuration
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # URL routing
│   └── wsgi.py                     # WSGI configuration
│
├── core/                            # Main application
│   ├── management/
│   │   └── commands/
│   │       └── seed_db.py          # Database seeding command
│   │
│   ├── authentication.py            # DRF authentication adapter
│   ├── middleware.py               # JWT validation middleware
│   ├── permissions.py              # RBAC permission classes
│   ├── models.py                   # Database models
│   ├── views.py                    # API ViewSets and Views
│   ├── serializers.py              # DRF serializers
│   ├── tests.py                    # Unit and integration tests
│   └── apps.py                     # App configuration
│
├── index.html                       # Frontend dashboard
├── manage.py                        # Django management utility
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## Security Considerations

### Password Security

- Passwords are hashed using Bcrypt algorithm with automatic salt generation
- Plaintext passwords are never stored or logged
- Password validation enforces minimum complexity requirements

### Token Security

- JWT tokens include signature verification
- Tokens have configurable expiration times
- Bearer tokens are transmitted only over HTTPS in production

### Access Control

- Role-based access is enforced at middleware level
- Permission checks occur before business logic execution
- Unauthorized access attempts are logged and rejected with appropriate HTTP status codes

### Production Recommendations

1. **Enable HTTPS**: Always use SSL/TLS in production environments
2. **Environment Variables**: Store secrets in environment variables, not in code
3. **Database**: Use PostgreSQL or similar enterprise database instead of SQLite
4. **Logging**: Implement centralized logging and monitoring
5. **CORS Configuration**: Configure CORS appropriately for your frontend domain
6. **Rate Limiting**: Implement rate limiting to prevent abuse

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guide
- All tests pass
- New features include corresponding tests
- Documentation is updated

---

## Troubleshooting

### Common Issues

**Q: "ModuleNotFoundError" when running the server**
- Ensure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Q: Token validation fails**
- Verify the token hasn't expired
- Check that the `SECRET_KEY` in settings matches token signing key
- Ensure `Authorization` header uses correct format: `Bearer <token>`

**Q: Permission denied errors**
- Verify user role has appropriate permissions in database
- Check that permissions are configured for the resource and HTTP method
- Review RBAC permission configuration

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Alexander Trofimov**  
Full-stack Python Developer  
[GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)

---

## Acknowledgments

- Django and Django REST Framework communities
- drf-spectacular for excellent API documentation
- Bootstrap team for the UI framework

---

**Last Updated**: January 2026  
**Version**: 1.0.0