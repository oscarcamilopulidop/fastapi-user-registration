# User Registration Service

This is a user registration service built with Python and FastAPI. It includes features such as signup, login, and user verification.

## Project Structure

The project has the following structure:

```
app/
    - config/               # Database configuration
    - middleware/           # Middleware component
    - repository/           # Database access layer
    - routers/              # Route definitions
    - schemas/              # Pydantic schemas
    - services/             # Business logic
    - tests/                # Unit tests
    - utils/                # Utility functions
.env                        # Environment variables
.gitignore                  # Specifies files to ignore in version control
README.md                   # This file
requirements.txt            # Python dependencies
init.sql                    # SQL script to initialize the database
Dockerfile                  # Defines the Docker image for the app
docker-compose.yml          # Defines the services that make up the app
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/oscarcamilopulidop/fastapi-user-registration.git
```

2. Build the Docker images:

```bash
docker-compose build
```

3. Start the services:

```bash
docker-compose up
```

The application will be available at `http://localhost:8000`.

You can interact with the application's API through the Swagger UI, which is accessible at `http://localhost:8000/docs`. The Swagger UI provides a user-friendly interface to explore and test the API endpoints.

MailHog is a development tool for SMTP testing. It captures and displays emails sent by the application. You can view these emails by navigating to `http://localhost:8025`.
## Testing

To run the tests, use the following command:

```bash
docker-compose run web pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

