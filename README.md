# DrinkLink

A QR-accessible, single-page menu application for restaurants and bars. Guests get a simple, visually clean drink menu with powerful filtering. Staff get a streamlined admin interface for adding/updating items with automated metadata suggestions.

## Tech Stack

### Frontend

- **Vue 3** (Composition API) with Vite
- **Vue Router** for routing
- **Pinia** for state management
- **TailwindCSS** for styling
- **Axios** for API calls

### Backend

- **FastAPI** (Python)
- **PostgreSQL** database
- **SQLAlchemy** ORM
- **Pydantic** for validation
- **Alembic** for migrations

### Infrastructure

- **Docker** & docker-compose
- **nginx** reverse proxy (production)

## Features

### Public Menu

- Beautiful grid layout of drinks (drafts, bottles, wines)
- Tag-based filtering (hoppy, dry, crisp, sweet, malty, etc.)
- Category filters (Drafts / Bottles / Wine)
- Sorting by ABV, Price, Name
- Quick search bar
- Item detail modal

### Admin Dashboard

- CRUD operations for menu items
- Tag manager
- Auto-suggest metadata from descriptions
- Inline editable table
- One-tap publish/unpublish toggle

### Backend Intelligence

- Automatic tag suggestion from keywords
- Derives tags from descriptions (e.g., "pine" → hoppy, "oak" → oaky)
- Auto-populate strength from ABV
- Search, filter, and sort endpoints

## Quick Start

### Development

1. Clone the repository:

```bash
git clone git@github.com:ryanlong1004/drinklink.git
cd drinklink
```

2. Start all services:

```bash
docker-compose up -d
```

3. Run database migrations:

```bash
docker-compose exec backend alembic upgrade head
```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - PgAdmin: http://localhost:5050 (run with `docker-compose --profile admin up`)

### Without Docker

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
drinklink/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Config, security
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Vue components
│   │   ├── views/        # Page views
│   │   ├── stores/       # Pinia stores
│   │   ├── router/       # Vue Router
│   │   └── services/     # API services
│   ├── Dockerfile.dev
│   └── package.json
└── docker-compose.yml
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## License

MIT
