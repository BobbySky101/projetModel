# Recipe Manager Module - Tests

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.recipe_manager.recipe_service import RecipeService


class TestRecipeManagerModule:
    """Test class for Recipe Manager module"""
    
    def __init__(self):
        self.service = RecipeService(api_key='TEST_API_KEY')
        
    def test_search_recipes(self):
        """Test recipe search functionality"""
        try:
            results = self.service.search_recipes('chicken')
            
            if results:
                print(f"? Test search_recipes: Found {len(results)} recipes")
                return True
            else:
                print("? Test search_recipes: No recipes found (may be API rate limit)")
                return False
        except Exception as e:
            print(f"? Test search_recipes failed: {e}")
            return False
    
    def test_get_recipe_by_id(self):
        """Test fetching recipe by ID"""
        try:
            # Use a known public recipe ID
            recipe_data = self.service.get_recipe_by_id(1037)
            
            if recipe_data:
                print(f"? Test get_recipe_by_id: Retrieved {recipe_data.get('title', 'Unknown')}")
                return True
            else:
                print("? Test get_recipe_by_id: Recipe not found")
                return False
        except Exception as e:
            print(f"? Test get_recipe_by_id failed: {e}")
            return False
    
    def test_import_from_url(self):
        """Test URL import functionality"""
        try:
            # Use a known public recipe ID in Spoonacular format
            test_url = f"https://api.spoonacular.com/recipes/full/1037"
            
            imported_recipe = self.service.import_from_url(test_url)
            
            if imported_recipe:
                print(f"? Test import_from_url: Successfully imported {imported_recipe.get('title', 'Unknown')}")
                return True
            else:
                print("? Test import_from_url: Failed to import from URL")
                return False
        except Exception as e:
            print(f"? Test import_from_url failed: {e}")
            return False
    
    def test_create_recipe_object(self):
        """Test creating Recipe objects from API data"""
        try:
            # Create a complete recipe dictionary
            test_data = {
                'id': 1234,
                'title': 'Test Recipe',
                'description': 'A test recipe',
                'image': 'https://example.com/image.jpg',
                'ingredients': [
                    {'quantity': 1, 'unit': 'cup', 'name': 'test ingredient'}
                ],
                'instructions': [
                    {'steps': ['Test step 1']}
                ]
            }
            
            recipe_obj = self.service.create_recipe_object(test_data)
            
            if recipe_obj:
                print(f"? Test create_recipe_object: Created object with title '{recipe_obj.title}'")
                return True
            else:
                print("? Test create_recipe_object: Failed to create Recipe object")
                return False
        except Exception as e:
            print(f"? Test create_recipe_object failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and report results"""
        print("Starting Recipe Manager Module Tests...")
        print("=" * 50)
        
        tests = [
            ("test_search_recipes", self.test_search_recipes),
            ("test_get_recipe_by_id", self.test_get_recipe_by_id),
            ("test_import_from_url", self.test_import_from_url),
            ("test_create_recipe_object", self.test_create_recipe_object),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
            except Exception as e:
                print(f"? {test_name} raised exception: {e}")
                results[test_name] = False
        
        # Print summary
        print("=" * 50)
        print(f"\\nTest Summary: {len(results)} tests run")
        passed = sum(1 for r in results.values() if r)
        failed = len(results) - passed
        
        print(f"Passed: {passed}/{len(results)}")
        print(f"Failed: {failed}/{len(results)}")
        
        if passed == len(results):
            print("\\n? All tests passed!")
        else:
            print(f"\\n? Some tests failed ({failed} failures)")
        
        return passed == len(results)


if __name__ == '__main__':
    test_runner = TestRecipeManagerModule()
    success = test_runner.run_all_tests()
    
    sys.exit(0 if success else 1)
