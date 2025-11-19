#!/bin/bash
# Script to update DrinkLink on Synology NAS

echo "=== DrinkLink Update Script for Synology ==="
echo ""

# Stop containers
echo "1. Stopping containers..."
docker compose -f docker-compose.synology.yml down

# Remove old images to force pull
echo "2. Removing old images..."
docker rmi saltycatfish/drinklink-frontend:latest 2>/dev/null || echo "  (Frontend image not found or already removed)"
docker rmi saltycatfish/drinklink-backend:latest 2>/dev/null || echo "  (Backend image not found or already removed)"

# Pull latest images
echo "3. Pulling latest images..."
docker compose -f docker-compose.synology.yml pull

# Start containers
echo "4. Starting containers..."
docker compose -f docker-compose.synology.yml up -d

# Wait a moment
sleep 5

# Show status
echo ""
echo "=== Container Status ==="
docker compose -f docker-compose.synology.yml ps

# Show frontend image info
echo ""
echo "=== Frontend Image Info ==="
docker images saltycatfish/drinklink-frontend:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}"

echo ""
echo "=== Frontend container logs (last 10 lines) ==="
docker logs drinklink-frontend --tail 10

echo ""
echo "✅ Update complete!"
echo "Access your app at: http://YOUR_NAS_IP:3080"
echo ""
echo "If you still see localhost:8000 errors:"
echo "1. Wait 30 seconds for nginx to start"
echo "2. Clear ALL browser data for this site"
echo "3. Try a different browser"
