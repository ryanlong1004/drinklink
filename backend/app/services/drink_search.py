import httpx


class DrinkDatabaseService:
    """
    Service to search external drink databases and return structured data.
    """

    BEER_STYLES = {
        "ipa": ["hoppy", "citrus"],
        "pale ale": ["hoppy", "citrus"],
        "lager": ["crisp", "light"],
        "pilsner": ["crisp", "light"],
        "stout": ["malty", "rich"],
        "porter": ["malty", "rich"],
        "wheat": ["light", "fruity"],
        "hefeweizen": ["fruity", "sweet"],
        "amber": ["malty"],
        "blonde": ["light", "sweet"],
        "sour": ["tart", "fruity"],
        "saison": ["dry", "fruity"],
    }

    @staticmethod
    async def search_beers(query: str) -> list[dict]:
        """
        Search Open Brewery DB for breweries and construct beer data.
        This is a simplified example - in production, you'd use a proper beer API.
        """
        results = []

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Search breweries
                response = await client.get(
                    "https://api.openbrewerydb.org/v1/breweries",
                    params={"by_name": query, "per_page": 10},
                )

                if response.status_code == 200:
                    breweries = response.json()

                    for brewery in breweries[:5]:  # Limit to 5 results
                        # Construct a generic beer entry from brewery data
                        result = {
                            "id": f"brewery_{brewery.get('id')}",
                            "name": f"{brewery.get('name', 'Unknown')} Flagship Ale",
                            "type": "Beer",
                            "style": brewery.get("brewery_type", "").title(),
                            "description": (
                                f"A signature beer from {brewery.get('name')}. "
                                f"Located in {brewery.get('city', '')}, "
                                f"{brewery.get('state', '')}."
                            ),
                            "abv": 5.5,  # Default estimate
                            "volume": "12 oz",
                            "origin": (
                                f"{brewery.get('city', '')}, "
                                f"{brewery.get('state', '')}, "
                                f"{brewery.get('country', 'USA')}"
                            ),
                            "producer": brewery.get("name", "Unknown Brewery"),
                            "brewery": brewery.get("name", "Unknown Brewery"),
                            "suggested_price": 6.50,
                            "suggested_category_id": None,
                            "suggested_tag_ids": [],
                            "image_url": "",
                            "website": brewery.get("website_url", ""),
                        }
                        results.append(result)

        except Exception as e:
            print(f"Error searching beer database: {e}")

        return results

    @staticmethod
    def create_mock_results(query: str) -> list[dict]:
        """
        Create mock search results based on common drinks.
        This is a fallback for demo purposes.
        """
        query_lower = query.lower()

        # Sample database of popular drinks
        mock_db = [
            {
                "id": "mock_1",
                "name": "Sierra Nevada Pale Ale",
                "type": "Beer",
                "style": "American Pale Ale",
                "description": (
                    "Pale Ale began as a home brewer's dream, "
                    "grew into an icon, and inspired countless brewers "
                    "to follow a passion of their own."
                ),
                "abv": 5.6,
                "volume": "12 oz",
                "origin": "California, USA",
                "producer": "Sierra Nevada Brewing Co.",
                "suggested_price": 6.00,
                "suggested_tag_ids": [],
            },
            {
                "id": "mock_2",
                "name": "Dogfish Head 60 Minute IPA",
                "type": "Beer",
                "style": "IPA",
                "description": (
                    "A session IPA continually hopped to deliver "
                    "a pungently, citrusy, grassy hop flavor."
                ),
                "abv": 6.0,
                "volume": "12 oz",
                "origin": "Delaware, USA",
                "producer": "Dogfish Head Craft Brewery",
                "suggested_price": 7.00,
                "suggested_tag_ids": [],
            },
            {
                "id": "mock_3",
                "name": "Left Hand Milk Stout",
                "type": "Beer",
                "style": "Milk Stout",
                "description": (
                    "A complex, black body with a brown head. "
                    "Rich roasted coffee and dark chocolate aroma."
                ),
                "abv": 6.0,
                "volume": "12 oz",
                "origin": "Colorado, USA",
                "producer": "Left Hand Brewing Company",
                "suggested_price": 6.50,
                "suggested_tag_ids": [],
            },
        ]

        # Filter results based on query
        results = [
            drink
            for drink in mock_db
            if query_lower in drink["name"].lower()
            or query_lower in drink["style"].lower()
            or query_lower in drink["producer"].lower()
        ]

        return results

    @staticmethod
    async def search_drinks(query: str) -> list[dict]:
        """
        Main search method that tries multiple sources.
        """
        results = []

        # Try external API first
        beer_results = await DrinkDatabaseService.search_beers(query)
        results.extend(beer_results)

        # If no results from API, use mock data
        if not results:
            mock_results = DrinkDatabaseService.create_mock_results(query)
            results.extend(mock_results)

        return results
