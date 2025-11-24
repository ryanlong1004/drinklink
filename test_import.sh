#!/bin/bash

# Test import endpoint locally

# Wait for backend
sleep 5

# Login (using default credentials)
echo "Logging in..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"change-me-in-production"}' | jq -r '.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "Login failed - checking if credentials work..."
  # Try to access categories to see if API is up
  curl -s http://localhost:8000/api/v1/categories | jq '.[0:2]'
  exit 1
fi

echo "Logged in successfully with token: ${TOKEN:0:20}..."

# Test import
echo -e "\nTesting import of wines..."
curl -s -X POST http://localhost:8000/api/v1/data/import \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @wines_to_add.json | jq '.'

echo -e "\nChecking items..."
curl -s http://localhost:8000/api/v1/items?limit=100 | jq '.items | length'
