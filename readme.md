# Movie management Systems

A brief description of your Django application goes here. Describe its purpose, features, and any other relevant details.

## Features

- User authentication (login, registration, etc.)
- Movie management (create, view, update, rate)
- Reporting functionality
- Admin controls

## Technologies Used

- Django
- Django REST Framework
- Python 3.x

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Anisujjaman-Md/Movie-management-Systems.git
   cd Movie-management-Systems
   ```

2. Build and start the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Running Migrations

If your application requires database migrations, you can run the following command after the containers are up:

```bash
docker-compose exec web python manage.py migrate
```

### Creating a Superuser

To create an admin user for the Django admin panel, run:

```bash
docker-compose exec web python manage.py createsuperuser
```

## Usage

Once the application is running, you can access the following endpoints (adjust based on your actual endpoints):

- `POST /api/login/` - Log in a user
- `POST /api/register/` - Register a new user
- `GET /api/movies/` - List all movies
- `POST /api/movies/` - Create a new movie (authenticated users only)
- `GET /api/movies/<id>/` - View details of a specific movie
- `PUT /api/movies/<id>/` - Update a specific movie (creator only)
- `POST /api/movies/<id>/rate/` - Rate a movie
- `POST /api/movies/<int:movie_id>/report/` - Report a movie
- `POST /api/reports/` - Reported Movie List
- `POST /api/reports/<int:pk>/status/` - Report a Status Update


## Admin Controls

Admin users can manage reported movies through the Django admin interface at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).
