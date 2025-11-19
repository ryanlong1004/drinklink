#!/bin/bash
# Force update script - completely removes containers and images

echo "=== FORCE UPDATE DrinkLink on Synology ==="
echo "This will completely remove and recreate all containers"
echo ""

# Stop and remove containers
echo "1. Stopping and removing containers..."
docker compose -f docker-compose.synology.yml down -v

# Remove ALL drinklink images (not just latest tag)
echo "2. Removing ALL DrinkLink images..."
docker images | grep drinklink | awk '{print $3}' | xargs -r docker rmi -f

# Prune to be extra sure
echo "3. Pruning unused images..."
docker image prune -f

# Pull fresh images
echo "4. Pulling fresh images from DockerHub..."
docker compose -f docker-compose.synology.yml pull

# Start containers
echo "5. Starting containers..."
docker compose -f docker-compose.synology.yml up -d

# Wait for startup
echo "6. Waiting for containers to start..."
sleep 10

# Show status
echo ""
echo "=== Container Status ==="
docker compose -f docker-compose.synology.yml ps

echo ""
echo "=== Backend Image Info ==="
docker images saltycatfish/drinklink-backend:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}"

echo ""
echo "=== Frontend Image Info ==="
docker images saltycatfish/drinklink-frontend --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}"

echo ""
echo "=== Backend Logs (last 15 lines) ==="
docker logs drinklink-backend --tail 15

echo ""
echo "✅ Force update complete!"
echo ""
echo "Now run: ./check-synology.sh"
echo "To verify data.py exists in the backend container"
