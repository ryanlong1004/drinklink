# Drink Search Feature

## Overview

The drink search feature allows administrators to quickly add new items by searching an external drink database. This streamlines the process of adding new items by auto-populating all the necessary data.

## How It Works

### Backend Components

1. **DrinkDatabaseService** (`backend/app/services/drink_search.py`)

   - Searches the Open Brewery DB API for brewery/beer data
   - Falls back to mock data if API is unavailable
   - Returns structured data matching the ItemCreate schema

2. **Search Endpoint** (`/api/v1/items/search-database`)
   - GET endpoint requiring authentication
   - Query parameter: `q` (minimum 2 characters)
   - Returns: `{ results: [...], total: n }`

### Frontend Components

1. **ItemSearch.vue** (`frontend/src/components/admin/ItemSearch.vue`)

   - Modal component with search bar
   - Displays search results in a grid
   - Each result shows: name, style, description, ABV, origin, producer
   - "Add Item" button on each result

2. **Integration in AdminItems.vue**
   - "🔍 Search Database" button in the toolbar
   - Opens ItemSearch modal
   - Selected items pre-populate the ItemForm

## Usage

1. Navigate to the Admin Items page
2. Click "🔍 Search Database" button
3. Type a search query (e.g., "pale ale", "IPA", "stout")
4. Press Enter or wait for results
5. Click "Add Item" on any result
6. The ItemForm will open with pre-populated data:
   - Name
   - Description
   - ABV
   - Volume (default: "12 oz")
   - Origin
   - Producer
   - Suggested price
7. Review and adjust the data as needed
8. Select category and tags
9. Save the item

## Data Sources

### Primary: Open Brewery DB API

- Endpoint: `https://api.openbrewerydb.org/v1/breweries`
- Provides real brewery and beer data
- Free, no API key required

### Fallback: Mock Data

If the API is unavailable, the system provides three mock beers:

- Sierra Nevada Pale Ale (5.6% ABV, California)
- Dogfish Head 60 Minute IPA (6.0% ABV, Delaware)
- Left Hand Milk Stout (6.0% ABV, Colorado)

## Technical Details

### Dependencies

- `httpx==0.25.2` - Async HTTP client for API calls

### API Response Structure

```json
{
  "results": [
    {
      "id": "string",
      "name": "string",
      "type": "Beer",
      "style": "string",
      "description": "string",
      "abv": 5.6,
      "volume": "12 oz",
      "origin": "string",
      "producer": "string",
      "suggested_price": 6.0,
      "suggested_tag_ids": []
    }
  ],
  "total": 1
}
```

### Authentication

The search endpoint requires admin authentication. The frontend automatically includes the JWT token from localStorage.

## Future Enhancements

Potential improvements for the search feature:

- Support for additional drink databases (wine, spirits, cocktails)
- Advanced filtering (by style, ABV range, origin)
- Automatic tag suggestion based on drink attributes
- Image URLs from external sources
- Batch import of multiple items
- Search history and favorites
- Price recommendations based on market data
