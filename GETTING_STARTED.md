# DrinkLink - Getting Started

## Quick Start

### Prerequisites

- Docker and Docker Compose
- (Optional) Node.js 18+ and Python 3.11+ for local development

### Setup with Docker (Recommended)

1. **Clone and setup:**

   ```bash
   cd drinklink
   chmod +x setup.sh
   ./setup.sh
   ```

   Or use Make:

   ```bash
   make setup
   ```

2. **Access the application:**

   - **Frontend (Public Menu):** http://localhost:3000
   - **Backend API:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs
   - **Admin Dashboard:** http://localhost:3000/admin

3. **Default Admin Credentials:**
   - Username: `admin`
   - Password: `change-me-in-production`

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb drinklink  # Create PostgreSQL database
alembic upgrade head  # Run migrations

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Project Structure

```
drinklink/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── items.py      # Item CRUD + search/filter
│   │   │       │   ├── categories.py # Category management
│   │   │       │   ├── tags.py       # Tag management
│   │   │       │   └── auth.py       # Authentication
│   │   │       └── router.py
│   │   ├── core/           # Core config
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/         # SQLAlchemy models
│   │   │   └── item.py     # Item, Category, Tag
│   │   ├── schemas/        # Pydantic schemas
│   │   │   ├── item.py
│   │   │   └── auth.py
│   │   ├── services/       # Business logic
│   │   │   └── tag_suggestion.py  # Auto-tag engine
│   │   └── main.py         # FastAPI app
│   ├── alembic/            # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── admin/      # Admin components
│   │   │   ├── FilterBar.vue
│   │   │   ├── ItemCard.vue
│   │   │   ├── ItemModal.vue
│   │   │   └── Pagination.vue
│   │   ├── views/
│   │   │   ├── MenuView.vue
│   │   │   ├── AdminView.vue
│   │   │   └── LoginView.vue
│   │   ├── stores/         # Pinia stores
│   │   │   ├── menu.js
│   │   │   ├── admin.js
│   │   │   └── auth.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── services/
│   │   │   └── api.js      # Axios API client
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css       # Tailwind styles
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── package.json
├── docker-compose.yml
├── setup.sh
├── Makefile
└── README.md
```

## Key Features

### Public Menu Interface

- ✅ Responsive grid layout of drinks
- ✅ Filter by categories (Drafts, Bottles, Wine)
- ✅ Filter by multiple tags (hoppy, citrusy, dry, etc.)
- ✅ Search by name, description, producer
- ✅ Sort by name, price, ABV, date
- ✅ Pagination
- ✅ Item detail modal with full information
- ✅ Mobile-optimized for QR code access

### Admin Dashboard

- ✅ CRUD operations for items
- ✅ One-click publish/unpublish toggle
- ✅ Category management
- ✅ Tag management with color customization
- ✅ Protected routes with JWT authentication

### Backend Intelligence

- ✅ **Auto-Tag Suggestion Engine**
  - Analyzes item descriptions and names
  - Suggests relevant tags (e.g., "pine" → hoppy)
  - Keywords mapped to taste profiles
  - ABV-based strength classification
- ✅ RESTful API with filtering, sorting, search
- ✅ Pagination support
- ✅ Published/draft status management

## API Endpoints

### Public Endpoints

```
GET  /api/v1/items              # List items (with filters)
GET  /api/v1/items/{id}         # Get item details
GET  /api/v1/categories         # List categories
GET  /api/v1/tags               # List tags
POST /api/v1/items/suggest-tags # Get tag suggestions
```

### Admin Endpoints (Requires Auth)

```
POST   /api/v1/auth/login       # Login
GET    /api/v1/auth/verify      # Verify token

POST   /api/v1/items            # Create item
PUT    /api/v1/items/{id}       # Update item
DELETE /api/v1/items/{id}       # Delete item

POST   /api/v1/categories       # Create category
PUT    /api/v1/categories/{id}  # Update category
DELETE /api/v1/categories/{id}  # Delete category

POST   /api/v1/tags             # Create tag
PUT    /api/v1/tags/{id}        # Update tag
DELETE /api/v1/tags/{id}        # Delete tag
```

### Query Parameters for Items

```
?page=1                  # Page number
?page_size=20            # Items per page
?category_id=1           # Filter by category
?tag_ids=1,2,3          # Filter by tags (AND logic)
?search=IPA             # Search in name/description/producer
?sort_by=price          # name, price, abv, created_at
?sort_order=asc         # asc or desc
?published_only=true    # Show only published items
```

## Development Commands

```bash
# Start all services
make up
# or
docker-compose up -d

# View logs
make logs
# or
docker-compose logs -f

# Stop services
make down

# Run migrations
make migrate

# Create new migration
make migrate-create

# Clean everything (including volumes)
make clean

# Rebuild containers
make rebuild
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# Backend
DATABASE_URL=postgresql://drinklink:password@localhost:5432/drinklink
SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password

# Frontend
VITE_API_URL=http://localhost:8000
```

### Tag Suggestion System

The tag suggestion engine analyzes text for keywords and maps them to tags:

**Examples:**

- "Pine and citrus hops" → **hoppy, citrusy**
- "Oak barrel aged" → **oaky**
- "Smooth and creamy stout" → **creamy, dark**
- "Refreshing session ale" → **light, sessionable**
- 8.5% ABV → **strong**
- 4.2% ABV → **sessionable**

Keywords are defined in `backend/app/services/tag_suggestion.py`.

## Database Schema

### Tables

- **items** - Menu items (drinks)
- **categories** - Item categories (Draft, Bottle, Wine)
- **tags** - Taste profile tags (hoppy, citrusy, etc.)
- **item_tags** - Many-to-many relationship

### Key Fields

- Items: name, description, price, abv, volume, producer, origin
- Tags: name, color (hex), description
- Categories: name, description, sort_order

## Deployment

### Production with Docker

1. Update `.env` with production values
2. Build and start:

   ```bash
   docker-compose -f docker-compose.yml up -d --build
   ```

3. The frontend will be served by nginx on port 80
4. API will be proxied through nginx

### Production Considerations

- Change `SECRET_KEY` and `ADMIN_PASSWORD`
- Set `ENVIRONMENT=production`
- Configure proper CORS origins
- Use PostgreSQL with proper credentials
- Set up SSL/TLS (Let's Encrypt)
- Configure backup strategy for database

## Troubleshooting

### Database connection issues

```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Recreate database
docker-compose down -v
docker-compose up -d
make migrate
```

### Frontend not connecting to backend

- Check `VITE_API_URL` in frontend/.env
- Verify backend is running on port 8000
- Check CORS settings in backend/app/core/config.py

### Migrations not working

```bash
# Reset migrations (development only)
docker-compose down -v
docker-compose up -d db
docker-compose exec backend alembic upgrade head
```

## Next Steps

1. **Enhance Admin UI:**

   - Complete CRUD forms for items/tags/categories
   - Add drag-and-drop sorting
   - Bulk operations
   - Image upload

2. **Additional Features:**

   - QR code generation per venue
   - Multi-venue support
   - Analytics dashboard
   - Customer favorites/ratings
   - Inventory management

3. **Optimization:**
   - Add caching (Redis)
   - Image optimization/CDN
   - Search optimization (Elasticsearch)
   - API rate limiting

## Support

For issues or questions, refer to:

- API Documentation: http://localhost:8000/docs
- GitHub Repository: https://github.com/ryanlong1004/drinklink

---

Built with ❤️ using FastAPI, Vue 3, PostgreSQL, and Docker
