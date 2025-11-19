#!/bin/bash

# DrinkLink Setup Script

echo "🍺 Setting up DrinkLink..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

# Run database migrations
echo "Running database migrations..."
docker-compose exec -T backend alembic upgrade head

# Create sample data (optional)
read -p "Do you want to create sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Creating sample data..."
    docker-compose exec -T backend python -c "
from app.core.database import SessionLocal
from app.models import Category, Tag, Item

db = SessionLocal()

# Create categories
categories = [
    Category(name='Draft Beer', slug='draft-beer', description='Fresh from the tap', sort_order=1),
    Category(name='Bottled Beer', slug='bottled-beer', description='Bottled selections', sort_order=2),
    Category(name='Wine', slug='wine', description='Red, white, and rosé', sort_order=3),
]
db.add_all(categories)
db.commit()

# Create tags
tags = [
    Tag(name='hoppy', slug='hoppy', description='Prominent hop character', color='#10B981'),
    Tag(name='citrusy', slug='citrusy', description='Bright citrus flavors', color='#F59E0B'),
    Tag(name='malty', slug='malty', description='Rich malt character', color='#8B4513'),
    Tag(name='light', slug='light', description='Light-bodied and crisp', color='#60A5FA'),
    Tag(name='dry', slug='dry', description='Crisp, clean finish', color='#A78BFA'),
]
db.add_all(tags)
db.commit()

print('✅ Sample data created!')
db.close()
"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Access the application at:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - PgAdmin: docker-compose --profile admin up -d && http://localhost:5050"
echo ""
echo "Default admin credentials:"
echo "  Username: admin"
echo "  Password: change-me-in-production"
echo ""
