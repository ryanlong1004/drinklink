import re
from typing import List, Dict, Set


class TagSuggestionService:
    """
    Service for automatically suggesting tags based on item descriptions and attributes.
    Uses keyword matching to infer appropriate tags.
    """

    # Keyword to tag mapping
    TAG_KEYWORDS: Dict[str, List[str]] = {
        # Hop characteristics
        "hoppy": ["hop", "hops", "hopped", "pine", "resinous", "dank", "piney"],
        "citrusy": [
            "citrus",
            "citrusy",
            "orange",
            "grapefruit",
            "lemon",
            "lime",
            "tangerine",
        ],
        "fruity": [
            "fruit",
            "fruity",
            "berry",
            "berries",
            "stone fruit",
            "tropical",
            "mango",
            "peach",
        ],
        # Malt characteristics
        "malty": ["malt", "malty", "bready", "bread", "biscuit", "toast", "toasted"],
        "caramel": ["caramel", "toffee", "butterscotch"],
        "roasted": ["roast", "roasted", "coffee", "chocolate", "cocoa"],
        # Body and mouthfeel
        "light": ["light", "crisp", "refreshing", "sessionable", "easy-drinking"],
        "full-bodied": ["full", "rich", "heavy", "robust", "thick"],
        "creamy": ["cream", "creamy", "smooth", "velvety", "silky"],
        # Taste profiles
        "bitter": ["bitter", "bitterness", "sharp"],
        "sweet": ["sweet", "sweetness", "dessert"],
        "dry": ["dry", "crisp", "clean"],
        "sour": ["sour", "tart", "acidic", "tangy"],
        "spicy": ["spice", "spicy", "pepper", "ginger", "cinnamon"],
        # Wine specific
        "oaky": ["oak", "oaked", "barrel", "wood", "woody"],
        "earthy": ["earth", "earthy", "mineral", "terroir"],
        "floral": ["floral", "flower", "flowery", "perfume", "rose", "violet"],
        "herbaceous": ["herb", "herbal", "grass", "grassy", "sage", "thyme"],
        # Beer styles
        "hazy": ["hazy", "cloudy", "murky", "unfiltered"],
        "dark": ["dark", "black", "porter", "stout"],
        "amber": ["amber", "copper", "red"],
        "pale": ["pale", "golden", "blonde"],
        # Strength
        "strong": ["strong", "high abv", "imperial", "double"],
        "sessionable": ["session", "sessionable", "easy-drinking", "drinkable"],
        # Origin/style
        "belgian": ["belgian", "belgium"],
        "german": ["german", "germany", "bavarian"],
        "american": ["american", "usa", "us"],
        "english": ["english", "british", "uk"],
        "ipa": ["ipa", "india pale ale"],
        "lager": ["lager"],
        "stout": ["stout"],
        "porter": ["porter"],
        "wheat": ["wheat", "hefeweizen", "witbier"],
    }

    @classmethod
    def suggest_tags_from_text(cls, text: str) -> Set[str]:
        """
        Analyze text and suggest appropriate tag names.

        Args:
            text: Description or name to analyze

        Returns:
            Set of suggested tag names
        """
        if not text:
            return set()

        text_lower = text.lower()
        suggested_tags = set()

        for tag_name, keywords in cls.TAG_KEYWORDS.items():
            for keyword in keywords:
                # Use word boundaries to avoid partial matches
                pattern = r"\b" + re.escape(keyword) + r"\b"
                if re.search(pattern, text_lower):
                    suggested_tags.add(tag_name)
                    break  # Found a match for this tag, move to next tag

        return suggested_tags

    @classmethod
    def suggest_tags_from_item(
        cls, name: str, description: str = None, abv: float = None, origin: str = None
    ) -> Set[str]:
        """
        Suggest tags based on multiple item attributes.

        Args:
            name: Item name
            description: Item description
            abv: Alcohol by volume
            origin: Country/region of origin

        Returns:
            Set of suggested tag names
        """
        suggested_tags = set()

        # Analyze name and description
        combined_text = f"{name or ''} {description or ''}"
        suggested_tags.update(cls.suggest_tags_from_text(combined_text))

        # Add origin-based tags
        if origin:
            suggested_tags.update(cls.suggest_tags_from_text(origin))

        # ABV-based suggestions
        if abv is not None:
            if abv < 4.5:
                suggested_tags.add("sessionable")
            elif abv > 7.5:
                suggested_tags.add("strong")

        return suggested_tags

    @classmethod
    def get_tag_description(cls, tag_name: str) -> str:
        """
        Get a suggested description for a tag based on its name.

        Args:
            tag_name: Name of the tag

        Returns:
            Suggested description
        """
        descriptions = {
            "hoppy": "Prominent hop character with pine or resinous notes",
            "citrusy": "Bright citrus flavors like orange, grapefruit, or lemon",
            "fruity": "Berry, stone fruit, or tropical fruit notes",
            "malty": "Rich malt character with bready or biscuit flavors",
            "caramel": "Sweet caramel or toffee notes",
            "roasted": "Dark roasted flavors like coffee or chocolate",
            "light": "Light-bodied, crisp, and refreshing",
            "full-bodied": "Rich, robust, and full-flavored",
            "creamy": "Smooth, velvety mouthfeel",
            "bitter": "Noticeable bitterness",
            "sweet": "Pleasant sweetness",
            "dry": "Crisp, clean finish with minimal sweetness",
            "sour": "Tart, acidic character",
            "spicy": "Spice notes from hops, yeast, or ingredients",
            "oaky": "Oak barrel aging character",
            "earthy": "Earthy, mineral notes",
            "floral": "Delicate floral aromatics",
            "herbaceous": "Herbal, grassy notes",
            "hazy": "Unfiltered, hazy appearance",
            "dark": "Dark color from roasted malts",
            "strong": "Higher alcohol content",
            "sessionable": "Easy-drinking, lower ABV for extended sessions",
        }

        return descriptions.get(tag_name, f"Characteristic: {tag_name}")
