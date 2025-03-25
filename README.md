# Salary Project

A salary calculator application built with FastAPI and SQLAlchemy.

## Prerequisites

- Python 3.13+
- Poetry for dependency management
- MariaDB 11.8+ (if running without Docker)

## Running with Docker

The easiest way to run the application is using Docker and Docker Compose, which will set up both the application and the database.

### Prerequisites for Docker

- Docker
- Docker Compose

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd salary-project
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

3. The application will be available at http://localhost:8000

4. To stop the application:
   ```bash
   docker-compose down
   ```

## Running without Docker

### Prerequisites

1. Python 3.13+
2. Poetry
3. MariaDB 11.8+

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd salary-project
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up a MariaDB database:
   - Create a database named `salary_calculator`
   - Create a user with access to this database
   - Update the `.env` file with your database connection details:
     ```
     DB_URL=mysql+aiomysql://user:password@localhost:3306/salary_calculator
     ```

4. Run database migrations:
   ```bash
   poetry run alembic upgrade head
   ```

5. Start the application:
   ```bash
   poetry run python main.py
   ```

6. The application will be available at http://localhost:8000

## Environment Configuration

The application uses the following environment variables:

- `DB_URL`: Database connection string (default: `mysql+aiomysql://user:password@localhost:3306/salary_calculator`)

You can modify these in the `.env` file for local development or in the `docker-compose.yml` file for Docker deployment.

## Development

### Code Quality

```bash
poetry run mypy .
poetry run ruff check .
```