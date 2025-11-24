#!/bin/bash

# Script to add wines via the DrinkLink API
# Usage: ./add_wines.sh

API_URL="http://drinklink.rlong.i234.me:3080/api/v1"

# Login to get token
echo "Enter admin username:"
read USERNAME
echo "Enter admin password:"
read -s PASSWORD

TOKEN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME&password=$PASSWORD" | jq -r '.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "Login failed"
  exit 1
fi

echo -e "\nLogin successful!\n"

# Get Wine category ID
WINE_CAT_ID=$(curl -s "$API_URL/categories" | jq -r '.[] | select(.name == "Wine") | .id')

if [ -z "$WINE_CAT_ID" ]; then
  echo "Wine category not found"
  exit 1
fi

echo "Wine category ID: $WINE_CAT_ID"

# Function to add a wine
add_wine() {
  local name="$1"
  local description="$2"
  local producer="$3"
  
  echo "Adding: $name"
  
  curl -s -X POST "$API_URL/items" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"$name\",
      \"description\": \"$description\",
      \"price\": 0.0,
      \"category_id\": $WINE_CAT_ID,
      \"producer\": \"$producer\",
      \"is_published\": true
    }" | jq -r '.name + " added with ID: " + (.id|tostring)'
}

# Add all wines
echo -e "\nAdding wines...\n"

add_wine "Sycamore Lane Pinot Grigio" "White wine with crisp, refreshing flavor" "Sycamore Lane"
add_wine "Sycamore Lane Cabernet Sauvignon" "Full-bodied red wine with rich flavor" "Sycamore Lane"
add_wine "Sycamore Lane Merlot" "Smooth red wine with soft tannins" "Sycamore Lane"
add_wine "Federalist Cabernet" "Bold Cabernet Sauvignon" "Federalist"
add_wine "Quilty Cabernet" "Premium Cabernet Sauvignon" "Quilty"
add_wine "The Show Malbec" "Argentinian Malbec with bold fruit flavors" "The Show"

echo -e "\nDone!"
