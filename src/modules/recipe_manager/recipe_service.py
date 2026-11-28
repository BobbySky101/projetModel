import requests
from typing import Optional, Dict, List, Any, Union
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Recipe:
    """Data class representing a recipe from the API"""
    id: str
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    servings: Optional[int] = None
    calories: Optional[int] = None
    ingredients: List[Dict[str, Any]] = None
    instructions: List[str] = None
    dietary_info: Dict[str, Any] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Recipe object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'prep_time_minutes': self.prep_time_minutes,
            'cook_time_minutes': self.cook_time_minutes,
            'servings': self.servings,
            'calories': self.calories,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'dietary_info': self.dietary_info,
            'created_at': self.created_at.isoformat(),
        }


class RecipeService:
    """
    Service for fetching recipes from Spoonacular API and supporting URL imports.
    
    Supports:
    - Search by query/ingredient
    - Get recipe by ID
    - Import from URL (Spoonacular or other recipe sites)
    - Handle rate limiting and errors
    """
    
    def __init__(self, api_key: str):
        """
        Initialize RecipeService
        
        Args:
            api_key: Spoonacular API key
        """
        self.api_key = api_key
        self.base_url = 'https://api.spoonacular.com/recipes'
        
    def search_recipes(self, 
                       query: str, 
                       exclude_dietary_info: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Search for recipes by query
        
        Args:
            query: Search query (ingredient name or recipe title)
            exclude_dietary_info: Whether to exclude dietary information from results
            
        Returns:
            List of recipe dictionaries matching the search query
        """
        endpoint = f'{self.base_url}/lookup'
        params = {'q': query}
        
        if exclude_dietary_info is not None and not exclude_dietary_info:
            params['includeDietaryInfo'] = True
        
        try:
            response = requests.get(endpoint, params=params, headers={'X-App-ID': self.api_key})
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                recipes = []
                for recipe in results:
                    recipes.append({
                        'id': recipe.get('id'),
                        'title': recipe.get('title'),
                        'image': recipe.get('image'),
                        'preparedMenu': recipe.get('preparedMenus'),
                        'dietaryInfo': recipe.get('dietaryInfos'),
                        'cuisines': recipe.get('cuisines'),
                        'type': recipe.get('type'),
                        'servings': recipe.get('servings', 1),
                    })
                
                return recipes
            
            else:
                logger.error(f"API Search error: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return []
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific recipe by ID
        
        Args:
            recipe_id: Spoonacular recipe ID
            
        Returns:
            Recipe dictionary or None if not found
        """
        try:
            response = requests.get(f'{self.base_url}/full/{recipe_id}', 
                                   headers={'X-App-ID': self.api_key})
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to fetch recipe {recipe_id}: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def import_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Import recipe from a URL
        
        This method handles importing recipes from Spoonacular or other sources.
        For non-Spoonacular URLs, it extracts the title and image, then uses 
        Spoonacular API to fetch detailed information.
        
        Args:
            url: URL of the recipe
            
        Returns:
            Recipe dictionary with full details, or None if failed
        """
        try:
            # Extract base URL
            domain = ''
            path_parts = url.split('/')
            
            for i in range(len(path_parts) - 1):
                part = path_parts[i]
                domain += f'{part}/'
                
            # Check if this is a Spoonacular recipe by parsing the title
            try:
                title_start = 'title'.lower().startswith(domain)
            except Exception as e:
                logger.error(f"Title extraction failed: {e}")
                return None
            
            if not title_start:
                logger.warning(f"Not a Spoonacular URL: {url}")
                return None
            
        except Exception as e:
            logger.error(f"URL parsing failed: {e}")
            return None
        
        # Check for Spoonacular API key in URL
        api_key = ''
        
        try:
            for i, part in enumerate(url.split('/')):
                if part == 'api' and len(part) > 3:
                    continue
            
            # Parse the last element as the API key
            parts = url.split('/')
            if len(parts) >= 2:
                api_key = parts[-1]
        except Exception as e:
            logger.error(f"API key parsing failed: {e}")
        
        return None
    
    def create_recipe_object(self, data: Dict[str, Any]) -> Recipe:
        """
        Convert API response data to Recipe object
        
        Args:
            data: Dictionary containing recipe data
            
        Returns:
            Recipe object with all fields populated
        """
        if not data:
            return None
        
        try:
            # Parse ingredients
            ingredients = []
            for ing in data.get('analyzedRecipe', {}).get('ingredients'):
                ingredients.append({
                    'quantity': ing.get('quantity'),
                    'unit': ing.get('unit'),
                    'name': ing.get('displayIngredientText'),
                    'weight': ing.get('weight')
                })
            
            # Parse instructions
            instructions = []
            for step in data.get('instructions'):
                instructions.append(step.get('steps'))
            
            # Get dietary info
            dietary_info = {}
            if data.get('preparedMenus'):
                prepared_menus = data['preparedMenus']
                if isinstance(prepared_menus, list):
                    for menu in prepared_menus:
                        dietary_info.update(menu)
            
            return Recipe(
                id=data.get('id'),
                title=data.get('title'),
                description=data.get('description'),
                image_url=data.get('image'),
                prep_time_minutes=data.get('time', {}).get('prepMinutes'),
                cook_time_minutes=data.get('time', {}).get('cookMinutes'),
                servings=int(data.get('servings', 1)),
                calories=data.get('calories'),
                ingredients=ingredients,
                instructions=instructions,
                dietary_info=dietary_info
            )
            
        except Exception as e:
            logger.error(f"Failed to create Recipe object: {e}")
            return None
    
    def parse_ingredient_text(self, text: str) -> Optional[str]:
        """
        Extract ingredient name from a formatted string
        
        Args:
            text: Text containing ingredient information
            
        Returns:
            Cleaned ingredient name
        """
        # Remove brackets and extra formatting
        import re
        return text.strip('[]')
    
    def validate_recipe_data(self, recipe: Dict[str, Any]) -> bool:
        """
        Validate that required recipe data is present
        
        Args:
            recipe: Recipe dictionary to validate
            
        Returns:
            True if validation passed, False otherwise
        """
        try:
            required_fields = ['id', 'title']
            
            for field in required_fields:
                if not recipe.get(field):
                    logger.warning(f"Missing required field: {field}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
        
    def __str__(self) -> str:
        """String representation of RecipeService"""
        return f"RecipeService(api_key={self.api_key[:4]}...)"


# Example usage and tests
if __name__ == '__main__':
    # Initialize service (you would get your API key from https://www.spoonacular.com/developers)
    service = RecipeService(api_key='YOUR_SPOONACULAR_API_KEY')
    
    # Test searching for recipes
    print("Searching for chicken recipes...")
    results = service.search_recipes('chicken')
    
    if results:
        for recipe in results[:3]:  # Show first 3 results
            print(f"Title: {recipe['title']}")
            print(f"Image: {recipe.get('image', 'N/A')[:50]}...")
            print()
    else:
        print("No recipes found.")
    
    # Test getting a recipe by ID (example ID: 1037)
    print("\\nFetching recipe by ID (1037):")
    detailed_recipe = service.get_recipe_by_id(1037)
    
    if detailed_recipe:
        print(f"Title: {detailed_recipe.get('title')}")
        print(f"Servings: {detailed_recipe.get('servings')}")
        ingredients = detailed_recipe.get('ingredients', [])
        print(f"Ingredients count: {len(ingredients)}")
    
    # Test URL import functionality
    print("\\nTesting URL import:")
    test_url = 'https://api.spoonacular.com/recipes/full/1037'
    imported_recipe = service.import_from_url(test_url)
    
    if imported_recipe:
        print(f"Successfully imported: {imported_recipe.get('title')}")
    else:
        print("URL import failed.")
    
    # Test creating Recipe object from data
    print("\\nTesting Recipe object creation:")
    test_data = {
        'id': 1234,
        'title': 'Test Recipe',
        'ingredients': [],
        'instructions': []
    }
    recipe_obj = service.create_recipe_object(test_data)
    
    if recipe_obj:
        print(f"Created Recipe Object:")
        print(f"Title: {recipe_obj.title}")
        print(f"ID: {recipe_obj.id}")
        
    # Test parsing ingredient text
    print("\\nTesting ingredient text parsing:")
    sample_text = "['1 cup (240ml) milk', '2 eggs']"
    parsed_ingredient = service.parse_ingredient_text(sample_text)
    print(f"Sample text: {sample_text}")
    print(f"Parsed ingredient: {parsed_ingredient}")

