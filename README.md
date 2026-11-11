# Stockroom — Multi-Tenant Warehouse Management System

A Django-based, multi-tenant warehouse management system designed to help multiple independent organizations manage their warehouses, products, inventory operations, and stock movements through a centralized web application.

Stockroom provides an organization-oriented architecture with strict tenant isolation, role-based access control, warehouse and product management, inventory tracking, stock operations, warehouse transfers, and a versioned REST API secured with organization-managed API keys.

The project is built with Django and PostgreSQL, follows a modular application structure, and is also Dockerized. It also includes automated tests and a GitHub Actions CI workflow.

---

## 🚀 Overview

Stockroom is a multi-tenant warehouse management application built to provide a structured and secure environment for businesses that need to manage inventory across multiple warehouses.

Unlike a traditional single-organization warehouse application, Stockroom allows multiple independent organizations to operate within the same application infrastructure.

Each organization has its own members, warehouses, products, inventory records, and API credentials.

The application enforces organization-level data isolation, ensuring that users can only access resources belonging to their own organization and according to their assigned permissions.

The system follows a modular Django architecture, separating business responsibilities into dedicated applications. This makes the codebase easier to maintain, extend, and develop independently.

Stockroom is primarily a server-rendered Django application, using Django Templates and Bootstrap for its web interface. A REST API is also provided for external integrations and programmatic inventory access.

### Project Goals

The main objectives behind Stockroom are:

- Implementing a practical multi-tenant architecture in Django.
- Enforcing organization-level data isolation.
- Designing role-based authorization for organization members.
- Managing multiple warehouses within independent organizations.
- Providing structured product and inventory management.
- Tracking stock operations and warehouse transfers.
- Maintaining data consistency during inventory operations.
- Exposing inventory information through a secured REST API.
- Implementing API key generation and management.
- Applying automated testing to critical application components.
- Using Docker for application containerization.
- Establishing an automated CI pipeline with GitHub Actions.

---

## ✨ Key Features

### Multi-Tenant Architecture
- Multiple independent organizations within one application.
- Organization-specific memberships and resources.
- Tenant-aware database queries and access control.
- Protection against cross-organization resource access.

### Organization Management
- Organization creation and management.
- Member management.
- Organization-specific membership roles.
- Member activation and removal.
- Manager-level administrative capabilities.

### Role-Based Access Control
- Three membership roles: Manager, Staff, and Viewer.
- Permission checks based on membership roles.
- Restricted organization management operations.
- Different access levels for different types of users.

### Warehouse Management
- Create and manage multiple warehouses.
- Warehouse details and location information.
- Active and inactive warehouse states.
- Warehouse-specific inventory.
- Warehouse-level stock operations.

### Product Management
- Organization-specific product catalog.
- Product creation and editing.
- Product descriptions.
- Flexible JSON-based product attributes.
- Product search, filtering, and pagination.
- Product details and inventory information.

### Inventory Management
- Stock-in operations.
- Stock-out operations.
- Inventory tracking.
- Stock movement records.
- Warehouse-to-warehouse transfers.
- Inventory calculations across warehouses.

### REST API
- Versioned API architecture.
- Django REST Framework integration.
- Custom API key authentication.
- Organization-scoped API access.
- Inventory quantity endpoint.
- OpenAPI schema generation.
- Interactive Swagger documentation.

### Development & Quality
- Modular Django application architecture.
- PostgreSQL database integration.
- Dockerized application environment.
- Automated Django tests.
- Git-based development workflow.
- GitHub Actions CI pipeline.

---

## 🛠 Technology Stack

The project uses the following technologies and libraries:

| Technology | Purpose |
|---|---|
| Python 3.13 | Main programming language |
| Django 6.1.2 | Backend web framework |
| Django Templates | Server-side rendering |
| Django REST Framework | REST API development |
| drf-spectacular | OpenAPI schema and API documentation |
| PostgreSQL 18 | Relational database |
| HTML5 | Web page structure |
| CSS3 | Styling |
| Bootstrap | Responsive user interface |
| JavaScript | Client-side interactions |
| Docker | Application containerization |
| Docker Compose | Multi-container environment |
| Git | Version control |
| GitHub | Source code hosting |
| GitHub Actions | Continuous Integration |
| Insomnia | API development and manual testing |

---

## 🏗 System Architecture

Stockroom follows a modular Django architecture in which each application is responsible for a specific business domain.

Instead of placing all business logic into a single Django application, the project separates functionality into independent applications.

This separation improves maintainability, reduces coupling, and makes future development easier.

### Application Responsibilities

| Application | Responsibility |
|---|---|
| `accounts` | User authentication and account-related functionality |
| `organizations` | Organizations, memberships, roles, authorization, and API key management |
| `dashboard` | Main dashboard and organization-level overview |
| `warehouses` | Warehouse creation, management, and status |
| `products` | Product catalog, product details, filtering, and pagination |
| `stock` | Inventory operations, stock movements, and transfers |
| `api` | REST API endpoints, authentication, permissions, and serializers |
| `config` | Django project configuration, settings, root URLs, and deployment entry points |

### Architectural Principles

The project emphasizes several important backend development principles:

**Separation of Concerns**

Each Django application handles a clearly defined responsibility.

**Tenant-Aware Data Access**

Database queries and authorization checks are designed around the active organization context.

**Centralized Business Logic**

Critical business operations are separated from presentation logic where appropriate.

**Service Layer**

Dedicated service logic is used for operations that require reusable business rules and controlled execution.

**Explicit Authorization**

Access control is enforced through authentication, membership validation, and role-based permission checks.

---

## 🏢 Multi-Tenancy Architecture

Multi-tenancy is one of the central architectural features of Stockroom.

The application allows multiple organizations to share the same application infrastructure while maintaining logical separation between their data.

Each organization operates independently.

For example:

- Organization A manages its own warehouses, products, members, and inventory.
- Organization B manages a completely separate set of resources.
- Members of Organization A cannot access the resources of Organization B.
- Organization-specific API credentials cannot be used to retrieve another organization's inventory.

### Tenant Isolation

Tenant isolation is enforced at the application level through organization-aware relationships, membership validation, and scoped database queries.

Every protected operation must respect the organization context of the authenticated user.

This applies to:

- Warehouse listings and details.
- Product listings and details.
- Inventory information.
- Stock operations.
- Warehouse transfers.
- Organization membership management.
- API inventory requests.

The system does not rely solely on frontend restrictions.

Authorization and tenant validation are handled on the backend, preventing users from bypassing access restrictions by manually changing URLs or submitting unauthorized requests.

### Shared Infrastructure, Independent Data

Organizations share the same Django application and PostgreSQL database infrastructure.

However, their business resources remain logically separated through organization relationships and backend authorization rules.

This approach provides a practical multi-tenant architecture without requiring a separate database or application instance for every organization.

---

## 👥 Organization & Membership Management

Organizations are the primary ownership boundary in Stockroom.

Each organization has its own membership records and business resources.

The organization management module provides functionality for managing members and controlling access to organization resources.

### Membership Features

- Organization membership management.
- Assigning membership roles.
- Viewing organization members.
- Adding members.
- Removing members.
- Managing membership permissions.
- Restricting sensitive operations to authorized users.

Membership roles determine what an authenticated user is allowed to do within an organization.

The authorization model is designed around the relationship between a user, an organization, and the user's assigned membership role.

---

## 🔐 Role-Based Access Control

Stockroom implements a three-level role-based access control system.

Each organization member is assigned one of the following roles:

### 1. Manager

The Manager has administrative control over the organization.

Manager capabilities include:

- Managing organization members.
- Assigning and managing membership roles.
- Managing organization-level settings and resources.
- Creating and managing API keys.
- Accessing restricted management operations.

### 2. Staff

Staff members are intended for operational activities.

Their role is designed around day-to-day warehouse and inventory management rather than organization administration.

### 3. Viewer

Viewers have a restricted access level intended for users who need visibility into organization information without administrative or operational management privileges.

### Authorization Enforcement

Role-based access control is implemented on the backend.

The application validates the authenticated user's membership and assigned role before allowing protected operations.

This prevents unauthorized users from accessing management functionality simply by navigating directly to a URL or submitting a crafted request.

---

## 🏬 Warehouse Management

Warehouse management allows each organization to maintain multiple warehouses within its own environment.

Warehouses represent independent physical or logical inventory locations.

### Warehouse Features

- Creating new warehouses.
- Viewing warehouse details.
- Editing warehouse information.
- Managing warehouse locations.
- Maintaining warehouse addresses.
- Activating and deactivating warehouses.
- Viewing warehouse-specific inventory information.
- Managing warehouse-related stock operations.

### Warehouse Status

Warehouses support active and inactive states.

This distinction is important for inventory management and stock calculations.

Inactive warehouses are excluded from the total inventory quantity returned by the inventory API.

Warehouse status is managed independently from the organization and its other warehouses.

---

## 📦 Product Management

The product management module provides organization-specific product catalog functionality.

Each organization maintains its own collection of products.

### Product Features

- Creating products.
- Viewing product details.
- Editing product information.
- Managing product descriptions.
- Supporting flexible product attributes.
- Searching products.
- Filtering product listings.
- Paginating product results.

### Flexible Product Attributes

Products support JSON-based attributes.

This provides flexibility when storing additional product-specific information without requiring a separate database column for every possible attribute.

Different businesses may have different product characteristics, and the flexible attribute structure helps accommodate those differences.

### Product Isolation

Products belong to their respective organizations.

A user cannot access or manage products belonging to another organization through unauthorized requests.

---

## 📊 Inventory Management

Inventory management is a core part of Stockroom.

The system tracks product quantities across an organization's warehouses and provides functionality for managing stock changes.

Inventory is associated with both products and warehouse locations.

This makes it possible to distinguish between the quantity of a product in one warehouse and its total quantity across the organization's inventory.

### Inventory Capabilities

- Tracking product quantities.
- Managing stock increases.
- Managing stock decreases.
- Recording stock movements.
- Supporting warehouse transfers.
- Retrieving product inventory information.
- Calculating inventory totals across warehouses.

### Organization-Level Inventory

Inventory information is scoped to the active organization.

A product's total inventory can be calculated across the organization's eligible warehouses without including inventory belonging to other organizations.

### Active Warehouse Consideration

Warehouse status is taken into account when calculating inventory totals through the REST API.

Only active warehouses contribute to the API's returned total inventory quantity.

---

## 🔄 Stock Operations

Stockroom supports operational inventory changes through stock-in and stock-out functionality.

These operations allow authorized users to increase or decrease product quantities in specific warehouses.

### Stock In

Stock-in operations increase the available quantity of a product in a selected warehouse.

Typical use cases include:

- Receiving new products.
- Adding newly purchased inventory.
- Recording incoming stock.
- Updating warehouse quantities after receiving goods.

### Stock Out

Stock-out operations decrease the available quantity of a product in a selected warehouse.

Typical use cases include:

- Removing inventory.
- Recording outgoing stock.
- Updating quantities after products leave a warehouse.

### Stock Movement Tracking

Stock operations are represented through inventory movement records.

These records provide a structured way to track changes in warehouse inventory rather than treating stock quantities as isolated values.

---

## 🚚 Warehouse Transfers

Stockroom supports transferring products between warehouses belonging to the same organization.

Warehouse transfers allow organizations to redistribute inventory between their warehouse locations.

### Transfer Workflow

A transfer involves:

1. Selecting the source warehouse.
2. Selecting the destination warehouse.
3. Selecting the product.
4. Specifying the quantity to transfer.
5. Processing the inventory movement.

Transfers are part of the inventory management workflow and allow organizations to maintain stock distribution across multiple warehouses.

Transfers are organization-scoped operations and must respect the organization's warehouse boundaries.

---

## 📈 Dashboard

Stockroom provides a centralized dashboard for organization-level visibility.

The dashboard offers an overview of important warehouse and product information.

### Dashboard Information

The dashboard includes:

- Total warehouse count.
- Total product count.
- Organization-level overview information.

The dashboard provides a starting point for navigating the application's main management sections.

---

## 🔌 REST API

Stockroom includes a versioned REST API built with Django REST Framework.

The API provides programmatic access to selected inventory information and is designed to support external applications and integrations.

The API is a complementary component of the warehouse management system rather than the primary interface of the project.

### API Architecture

The API follows a versioned URL structure:

`/api/v1/`

The implementation uses:

- Django REST Framework.
- Custom API key authentication.
- Organization-scoped access.
- Dedicated API serializers and views.
- Service-layer business logic.
- drf-spectacular for OpenAPI documentation.

### Available Endpoint

#### Retrieve Product Inventory

**Endpoint:**

`GET /api/v1/products/<sku>/inventory/`

This endpoint retrieves the total inventory quantity of a specified product within the authenticated API key's organization.

The calculation considers the organization's active warehouses.

Inactive warehouses are excluded from the returned inventory total.

### Endpoint Characteristics

- Requires API key authentication.
- Uses the API key's organization context.
- Prevents cross-organization inventory access.
- Retrieves inventory information by product SKU.
- Calculates total quantity across eligible warehouses.
- Excludes inactive warehouses from the total.

The endpoint is designed to expose inventory information without granting external applications unrestricted access to the internal management system.

### API Versioning

The API is organized under the `/api/v1/` prefix.

This provides a structured foundation for introducing additional endpoints and future API versions without changing the existing version's URL structure.

---

## 🔑 API Key Management

Stockroom implements an organization-oriented API key management system.

API keys provide external applications with an authentication mechanism for accessing protected API functionality.

API key management is integrated into the organization management interface.

### API Key Features

- Manager-only API key management.
- Creating named API keys.
- Generating unique API credentials.
- Displaying newly generated credentials.
- Deactivating existing API keys.
- Rejecting inactive API credentials.
- Organization-scoped API authentication.

### Key Generation

Managers can create API keys and assign descriptive names to identify their intended usage.

The generated raw key is displayed after creation so that it can be copied and used by an external application.

### Secure Storage

API keys are stored using hashed credentials rather than keeping the raw secret available in the database.

This reduces the risk of exposing usable API credentials if the database is compromised.

### API Key Deactivation

Managers can deactivate previously generated keys.

Once a key is inactive, it can no longer authenticate API requests.

This provides a way to revoke access without requiring changes to the API implementation.

### Organization-Scoped Authentication

Every API key is associated with an organization.

When an API request is authenticated, the organization associated with the key determines the data scope of the request.

This ensures that external integrations cannot use an API key belonging to one organization to retrieve another organization's inventory.

---

## 🛡 Security & Data Isolation

Security is an important part of Stockroom's architecture.

The project applies multiple layers of backend validation and access control.

### Authentication

Protected application functionality requires an authenticated user.

The REST API uses a dedicated API key authentication mechanism.

### Membership Validation

An authenticated user must have the appropriate organization membership to access organization-specific resources.

### Role-Based Authorization

Sensitive management operations are restricted according to membership roles.

### Tenant Isolation

Organization-aware queries prevent users from accessing resources belonging to other organizations.

### API Key Security

API keys are stored as hashed credentials and can be deactivated by authorized managers.

### Backend Enforcement

Authorization checks are performed on the server side rather than relying on frontend visibility or navigation restrictions.

This is particularly important in a multi-tenant system where unauthorized cross-organization access must be prevented.

---

## 🗄 Database & Data Integrity

Stockroom uses PostgreSQL as its relational database.

The database structure supports the relationships between:

- Users.
- Organizations.
- Memberships.
- Warehouses.
- Products.
- Inventory records.
- Stock movements.
- API keys.

### Relational Data Modeling

The application uses Django's ORM to manage database relationships and perform database operations.

Organization relationships are central to the data model and help enforce tenant ownership boundaries.

### Transactional Business Operations

Critical business operations use dedicated service logic and database transaction handling where required.

This helps keep related database changes consistent during multi-step operations.

### Database Migrations

Django migrations are used to manage database schema changes.

The CI workflow also checks for missing migrations before running the automated test suite.

---

## 🧪 Automated Testing

Stockroom includes an automated Django testing suite.

The project introduces automated testing as part of its development workflow, with particular emphasis on the organization management and authorization components.

### Current Test Coverage

The project currently includes **54 automated tests** focused on the `organizations` application.

These tests cover important organization-related functionality, including:

- Organization models.
- Membership behavior.
- Organization-related views.
- Service-layer functionality.
- Authorization rules.
- Tenant isolation.
- Organization-related deletion behavior.

The tests help verify that organization-level access restrictions and core membership logic behave as expected.

### Test Execution

The project's automated tests can be executed using Django's standard test command:

`python manage.py test`

Django's test discovery mechanism automatically discovers and executes recognized test modules across installed applications.

As additional tests are introduced into other applications, they can be included in the same test execution workflow without requiring changes to the CI command.

### Testing Scope

The current automated test suite is primarily focused on the organizations and multi-tenancy security domain.

Not every application and business workflow currently has dedicated automated test coverage.

---

## ⚙️ Continuous Integration

Stockroom uses GitHub Actions to automate important development checks.

The CI workflow is defined in:

`.github/workflows/ci.yaml`

The workflow is triggered by:

- Push events targeting the `main` branch.
- Pull requests targeting the `main` branch.

### CI Environment

The workflow uses:

| Component | Configuration |
|---|---|
| Operating System | Ubuntu |
| Python | 3.13 |
| Database | PostgreSQL 18 |
| Test Framework | Django Test Framework |

### CI Pipeline

The workflow performs the following steps:

**1. Repository Checkout**

Retrieves the latest repository contents.

**2. Python Setup**

Configures the Python environment using the selected Python version.

**3. Dependency Installation**

Installs project dependencies from `requirements.txt`.

**4. Django System Check**

Runs:

`python manage.py check`

This verifies the Django project's configuration for common issues.

**5. Migration Consistency Check**

Runs:

`python manage.py makemigrations --check --dry-run`

This checks whether model changes require new migrations.

**6. Database Migrations**

Runs:

`python manage.py migrate --noinput`

This applies the project's migrations to the PostgreSQL test database.

**7. Automated Tests**

Runs:

`python manage.py test`

This executes the discoverable Django automated test suite.

### CI Benefits

The automated workflow helps identify:

- Django configuration problems.
- Missing environment variables.
- Dependency installation issues.
- Database connectivity problems.
- Missing migrations.
- Automated test failures.

This provides an automated verification step whenever changes are pushed to the main development branch or submitted through a pull request.

---

## 🐳 Dockerization

Stockroom is Dockerized and designed to run in a containerized environment.

The project includes Docker configuration for the application and its PostgreSQL database dependency.

Docker Compose is used to coordinate the application and database services.

The containerized environment provides a more consistent runtime setup and reduces differences between development and deployment environments.

The project also includes an application entrypoint responsible for preparing the application environment before starting the Django server.

For complete Docker installation and execution instructions, refer to the [Docker Setup Guide](YOUR_DOCKER_GUIDE_URL).

---

## 📁 Project Structure

The repository is organized into the following main components:

```text
Multi-Tenant-Warehouse-Management/
│
├── .github/
│   └── workflows/
│       └── ci.yaml
│
└── config/
    │
    ├── accounts/
    │
    ├── api/
    │
    ├── dashboard/
    │
    ├── organizations/
    │
    ├── products/
    │
    ├── stock/
    │
    ├── warehouses/
    │
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── templates/
    │
    ├── static/
    │
    ├── project_screenshots/
    │
    ├── manage.py
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yaml
    └── entrypoint.sh
```

### Main Directories

**`.github/workflows/`**

Contains the GitHub Actions CI workflow.

**`accounts/`**

Handles user account and authentication functionality.

**`api/`**

Contains REST API functionality, API authentication, permissions, serializers, and API endpoints.

**`dashboard/`**

Provides the main dashboard interface.

**`organizations/`**

Contains organization and membership management, role-based authorization, and API key management.

**`products/`**

Handles product catalog functionality.

**`stock/`**

Handles inventory operations and stock movements.

**`warehouses/`**

Manages warehouse-related functionality.

**`config/`**

Contains the main Django project configuration.

**`templates/`**

Contains server-rendered HTML templates.

**`static/`**

Contains static frontend assets.

**`project_screenshots/`**

Contains screenshots of the application's interface and implemented functionality.

---

## 🔧 Environment Configuration

The application uses environment variables for configuration.

Important environment variables include:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_HOST` | PostgreSQL hostname |
| `POSTGRES_PORT` | PostgreSQL port |

These variables allow the application configuration to be separated from environment-specific values.

Sensitive values such as the Django secret key and database credentials should not be committed to the repository.

The CI workflow provides its own test-specific environment variables.

---

## 🌐 Application Routes

The main application sections are organized under the following URL prefixes:

| Route | Description |
|---|---|
| `/` | Main application entry point |
| `/admin/` | Django administration |
| `/dashboard/` | Main dashboard |
| `/organization/` | Organization management |
| `/products/` | Product management |
| `/stock/` | Inventory operations |
| `/warehouses/` | Warehouse management |
| `/api/v1/` | Versioned REST API |

### API Documentation Routes

| Route | Description |
|---|---|
| `/api/v1/schema/` | OpenAPI schema |
| `/api/v1/docs/` | Interactive Swagger API documentation |

---
