#!/bin/bash
# Diagnostic script to check Synology deployment

echo "=== Checking DrinkLink Deployment ==="
echo ""

echo "1. Container status:"
docker ps --filter "name=drinklink" --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
echo ""

echo "2. Backend image digest:"
docker images saltycatfish/drinklink-backend:latest --format "{{.ID}}\t{{.CreatedAt}}"
echo ""

echo "3. Frontend image digest:"
docker images saltycatfish/drinklink-frontend --format "{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}"
echo ""

echo "4. Check if data.py exists in backend container:"
docker exec drinklink-backend ls -la /app/app/api/v1/endpoints/data.py 2>/dev/null || echo "  ❌ data.py NOT FOUND"
echo ""

echo "5. Check if router includes data endpoints:"
docker exec drinklink-backend cat /app/app/api/v1/router.py | grep -A 2 "data"
echo ""

echo "6. Test backend directly (skip nginx):"
docker exec drinklink-backend wget -q -O- http://localhost:8000/api/v1/categories 2>/dev/null | head -c 100
echo ""
echo ""

echo "7. Check backend logs for errors:"
docker logs drinklink-backend --tail 20
